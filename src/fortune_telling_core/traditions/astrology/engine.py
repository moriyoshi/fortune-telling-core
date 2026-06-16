"""Astrology engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ExhaustedRngError, ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.astrology.aspects import (
    compute_aspects,
    compute_cross_aspects,
    render_aspects,
)
from fortune_telling_core.traditions.astrology.birth import parse_birth_data
from fortune_telling_core.traditions.astrology.bodies import POSITION_NAMES, Body
from fortune_telling_core.traditions.astrology.chart import cast_draw
from fortune_telling_core.traditions.astrology.config import ZodiacMode
from fortune_telling_core.traditions.astrology.spreads import NATAL_CHART
from fortune_telling_core.traditions.astrology.zodiac import SIDEREAL_ZODIAC, TROPICAL_ZODIAC


class _NullRng:
    kind = "null"

    def randint(self, low: int, high: int) -> int:
        del low, high
        raise ExhaustedRngError("AstrologyEngine.cast must not use randomness")

    def shuffle(self, n: int) -> list[int]:
        del n
        raise ExhaustedRngError("AstrologyEngine.cast must not use randomness")

    def random(self) -> float:
        raise ExhaustedRngError("AstrologyEngine.cast must not use randomness")


_NULL_RNG = _NullRng()


class AstrologyEngine(AbstractEngine):
    """Natal astrology engine using an injectable ephemeris.

    The engine casts deterministic natal charts. It ignores caller-supplied
    randomness and records the ephemeris, house system, and zodiac mode in
    reading provenance.

    When the request carries ``as_of``, the engine additionally computes the
    transiting bodies for that moment and appends transit-to-natal aspects to
    the summary. The natal chart is timeless, so without ``as_of`` the reading
    is the pure natal chart. Transit positions are stored on the draw, so a
    replay reproduces them without the ephemeris.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            When omitted, ``BuiltinEphemeris`` is used.
    """

    id = "astro.engine"
    version = "0.1.0"

    def __init__(self, ephemeris: Ephemeris | None = None) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the zodiac deck implied by the request.

        Args:
            request: Reading request containing birth data and optional
                ``zodiac`` configuration in options or querent attributes.

        Returns:
            ``SIDEREAL_ZODIAC`` when the request asks for sidereal astrology,
            otherwise ``TROPICAL_ZODIAC``.

        Raises:
            ValidationError: If required birth data or configuration is
                invalid.
        """

        birth = parse_birth_data(request)
        return SIDEREAL_ZODIAC if birth.config.zodiac == ZodiacMode.SIDEREAL else TROPICAL_ZODIAC

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the natal chart spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``NATAL_CHART.id``.

        Returns:
            The natal chart spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != NATAL_CHART.id:
            raise ValidationError(f"unsupported astrology spread: {request.spread_id}")
        return NATAL_CHART

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Cast the natal chart as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime``, ``latitude``,
                and ``longitude`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine``
                compatibility.

        Returns:
            A draw whose selections place bodies and angles in zodiac signs.

        Raises:
            ValidationError: If request birth data or chart configuration is
                invalid.
            EphemerisError: If the configured ephemeris cannot compute a
                required body.
        """

        del rng
        birth = parse_birth_data(request)
        return cast_draw(birth, self.ephemeris, transit_at=request.as_of)

    def cast(self, request: ReadingRequest) -> Reading:
        """Cast a natal chart without a caller RNG.

        Args:
            request: Reading request containing birth data and chart options.

        Returns:
            A reading with body placements and aspect summary.

        Raises:
            ValidationError: If request birth data or chart configuration is
                invalid.
            EphemerisError: If the configured ephemeris cannot compute a
                required body.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        longitudes = {
            position.selection.position_id: _modifier_float(position.selection, "longitude")
            for position in base.positions
            if self._include_in_aspects(request, position.selection.position_id)
        }
        natal = render_aspects(compute_aspects(longitudes))
        transit_at, transits = _transit_longitudes(draw)
        summary = _join_summaries(natal, _render_transits(transits, longitudes, transit_at))
        birth = parse_birth_data(request)
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            f"house_system={birth.config.house_system.value}",
            f"zodiac={birth.config.zodiac.value}",
            f"ayanamsa={'' if birth.config.ayanamsa is None else birth.config.ayanamsa.value}",
        )
        if transit_at is not None:
            notes = (*notes, f"transit_at={transit_at}")
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )

    def _include_in_aspects(self, request: ReadingRequest, position_id: str) -> bool:
        birth = parse_birth_data(request)
        if birth.config.include_angles_in_aspects:
            return True
        return position_id not in {"ascendant", "midheaven"}


def _modifier_float(selection: Selection, key: str) -> float:
    value = (selection.modifiers or {}).get(key)
    if value is None:
        raise ValidationError(f"selection modifier {key!r} is required")
    return float(value)


# The mirror node duplicates every aspect of its opposite, so it is omitted from
# the transiting set to avoid doubled lines.
_TRANSIT_EXCLUDED = frozenset({Body.SOUTH_NODE.value})


def _transit_longitudes(draw: Draw) -> tuple[str | None, dict[str, float]]:
    """Extract the transiting positions recorded in the draw.

    Returns the transit timestamp (``None`` when no transits were cast) and a
    map of position id to transit ecliptic longitude. Read from the draw so a
    replay reproduces transits without touching the ephemeris.
    """

    transit_at: str | None = None
    longitudes: dict[str, float] = {}
    for selection in draw.selections:
        modifiers = selection.modifiers or {}
        if "transit_at" in modifiers:
            transit_at = modifiers["transit_at"]
        raw = modifiers.get("transit_longitude")
        if raw is not None and selection.position_id not in _TRANSIT_EXCLUDED:
            longitudes[selection.position_id] = float(raw)
    return transit_at, longitudes


def _render_transits(
    transits: dict[str, float], natal: dict[str, float], transit_at: str | None
) -> str | None:
    if transit_at is None or not transits:
        return None
    transit_map = {f"transit {POSITION_NAMES[pid]}": lon for pid, lon in transits.items()}
    natal_map = {f"natal {POSITION_NAMES[pid]}": lon for pid, lon in natal.items()}
    return render_aspects(
        compute_cross_aspects(transit_map, natal_map),
        heading=f"Transits as of {transit_at}",
    )


def _join_summaries(*parts: str | None) -> str | None:
    present = [part for part in parts if part]
    return " ".join(present) if present else None


def build_engine(ephemeris: Ephemeris | None = None) -> AstrologyEngine:
    """Create a natal astrology engine.

    Args:
        ephemeris: Optional ephemeris backend. Defaults to the built-in
            pure-Python backend.

    Returns:
        A new ``AstrologyEngine`` instance.
    """

    return AstrologyEngine(ephemeris=ephemeris)
