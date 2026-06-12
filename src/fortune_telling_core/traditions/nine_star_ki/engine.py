"""Nine Star Ki engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.time_model import TimeModel, effective_datetime
from fortune_telling_core.draw import Draw
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.nine_star_ki.birth import parse_birth_data
from fortune_telling_core.traditions.nine_star_ki.chart import draw_from_chart
from fortune_telling_core.traditions.nine_star_ki.config import DayStarEscapement
from fortune_telling_core.traditions.nine_star_ki.deck import NINE_STAR_KI_DECK
from fortune_telling_core.traditions.nine_star_ki.spreads import NINE_STAR_KI_SPREAD
from fortune_telling_core.traditions.nine_star_ki.star_calc import compute_chart

_NULL_RNG = NullRng("NineStarKiEngine.cast must not use randomness")


class NineStarKiEngine(AbstractEngine):
    """Nine Star Ki engine using shared solar-term astronomy.

    The engine deterministically computes principal, monthly, daily, and
    tendency stars, then renders annual and monthly flying-star charts into
    the reading summary.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            Defaults to ``BuiltinEphemeris``.
        time_model: Default time adjustment model used when the request does
            not specify one.
        day_star_escapement: Default daily-star solstice reversal school used
            when the request does not specify ``day_star_escapement``.
        target_year: Default annual chart year. When omitted, the request year
            is used.
    """

    id = "ninestarki.engine"
    version = "0.1.0"

    def __init__(
        self,
        ephemeris: Ephemeris | None = None,
        *,
        time_model: TimeModel = TimeModel.CLOCK,
        day_star_escapement: DayStarEscapement = DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE,
        target_year: int | None = None,
    ) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()
        self.time_model = time_model
        self.day_star_escapement = day_star_escapement
        self.target_year = target_year

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Nine Star Ki deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``NINE_STAR_KI_DECK.id``.

        Returns:
            The bundled nine-star deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != NINE_STAR_KI_DECK.id:
            raise ValidationError(f"unsupported Nine Star Ki deck: {request.deck_id}")
        return NINE_STAR_KI_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Nine Star Ki spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``NINE_STAR_KI_SPREAD.id``.

        Returns:
            The bundled Nine Star Ki spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != NINE_STAR_KI_SPREAD.id:
            raise ValidationError(f"unsupported Nine Star Ki spread: {request.spread_id}")
        return NINE_STAR_KI_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute Nine Star Ki placements as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime``, ``latitude``,
                and ``longitude`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine``
                compatibility.

        Returns:
            A draw with natal and chart selections.

        Raises:
            ValidationError: If required birth data or options are invalid.
            EphemerisError: If the configured ephemeris cannot compute solar
                terms.
        """

        del rng
        birth = parse_birth_data(request, self.target_year, self.day_star_escapement)
        time_model = (
            birth.time_model
            if "time_model" in (request.options or {})
            or (request.querent and "time_model" in (request.querent.attributes or {}))
            else self.time_model
        )
        effective = effective_datetime(
            birth.birth_datetime, birth.longitude, time_model, self.ephemeris
        )
        return draw_from_chart(
            compute_chart(
                birth.birth_datetime,
                effective,
                self.ephemeris,
                birth.target_year,
                birth.day_star_escapement,
            )
        )

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Nine Star Ki chart without a caller RNG.

        Args:
            request: Reading request containing birth data and optional chart
                configuration.

        Returns:
            A reading with star placements and chart summary text.

        Raises:
            ValidationError: If required birth data or options are invalid.
            EphemerisError: If the configured ephemeris cannot compute solar
                terms.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        summary = _summary_from_draw(draw)
        first = dict(draw.selections[0].modifiers or {})
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            f"time_model={self.time_model.value}",
            "year_anchor=1900-1-white-risshun",
            f"day_star_escapement={first.get('day_star_escapement', '')}",
            f"target_year={first.get('target_year', '')}",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _summary_from_draw(draw: Draw) -> str:
    modifiers = dict(draw.selections[0].modifiers or {})
    return (
        f"Solar year {modifiers['solar_year']}: principal star {modifiers['year_star']}. "
        f"Solar month index {modifiers['solar_month_index']}: "
        f"monthly star {modifiers['month_star']}. "
        f"Daily star {modifiers['day_star']} ({modifiers['direction']}). "
        f"Tendency star {modifiers['tendency_star']}"
        f"{' (center case)' if modifiers['center_case'] == 'true' else ''}. "
        f"Annual chart {modifiers['target_year']}: {modifiers['annual_chart']}. "
        f"Monthly chart: {modifiers['monthly_chart']}."
    )


def build_engine(
    ephemeris: Ephemeris | None = None,
    *,
    time_model: TimeModel = TimeModel.CLOCK,
    day_star_escapement: DayStarEscapement = DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE,
    target_year: int | None = None,
) -> NineStarKiEngine:
    """Create a Nine Star Ki engine.

    Args:
        ephemeris: Optional ephemeris backend. Defaults to the built-in
            pure-Python backend.
        time_model: Default time adjustment model.
        day_star_escapement: Default daily-star solstice reversal school.
        target_year: Default annual chart year.

    Returns:
        A new ``NineStarKiEngine`` instance.
    """

    return NineStarKiEngine(
        ephemeris=ephemeris,
        time_model=time_model,
        day_star_escapement=day_star_escapement,
        target_year=target_year,
    )
