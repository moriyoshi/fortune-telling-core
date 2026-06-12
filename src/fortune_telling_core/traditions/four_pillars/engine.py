"""Four Pillars engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.draw import Draw
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.four_pillars.birth import parse_birth_data
from fortune_telling_core.traditions.four_pillars.chart import draw_from_pillars
from fortune_telling_core.traditions.four_pillars.config import DayBoundary, TimeModel
from fortune_telling_core.traditions.four_pillars.deck import FOUR_PILLARS_DECK
from fortune_telling_core.traditions.four_pillars.luck import annual_pillar_cjk, luck_pillars
from fortune_telling_core.traditions.four_pillars.pillars import compute_pillars
from fortune_telling_core.traditions.four_pillars.spreads import FOUR_PILLARS_SPREAD
from fortune_telling_core.traditions.four_pillars.ten_gods import (
    day_master_strength,
    element_distribution,
)
from fortune_telling_core.traditions.four_pillars.time_model import effective_datetime

_NULL_RNG = NullRng("FourPillarsEngine.cast must not use randomness")


class FourPillarsEngine(AbstractEngine):
    """Four Pillars engine using shared solar-term astronomy.

    The engine deterministically computes year, month, day, and hour pillars,
    then enriches the reading summary with element balance, Day Master
    strength, Luck Pillars, and the annual pillar.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            Defaults to ``BuiltinEphemeris``.
        time_model: Default time adjustment model used when the request does
            not specify one.
        day_boundary: Default day-boundary rule used when the request does
            not specify one.
        luck_count: Default number of Luck Pillars to render.
    """

    id = "fourpillars.engine"
    version = "0.1.0"

    def __init__(
        self,
        ephemeris: Ephemeris | None = None,
        *,
        time_model: TimeModel = TimeModel.CLOCK,
        day_boundary: DayBoundary = DayBoundary.MIDNIGHT,
        luck_count: int = 8,
    ) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()
        self.time_model = time_model
        self.day_boundary = day_boundary
        self.luck_count = luck_count

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Four Pillars stem and branch deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``FOUR_PILLARS_DECK.id``.

        Returns:
            The bundled stem and branch deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != FOUR_PILLARS_DECK.id:
            raise ValidationError(f"unsupported Four Pillars deck: {request.deck_id}")
        return FOUR_PILLARS_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the eight-position Four Pillars spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``FOUR_PILLARS_SPREAD.id``.

        Returns:
            The bundled Four Pillars spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != FOUR_PILLARS_SPREAD.id:
            raise ValidationError(f"unsupported Four Pillars spread: {request.spread_id}")
        return FOUR_PILLARS_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute Four Pillars as a deterministic draw.

        Args:
            request: Reading request with birth data. ``birth_datetime``,
                ``latitude``, ``longitude``, and ``gender`` are required in
                options or querent attributes.
            rng: Ignored. The argument is present for ``Engine``
                compatibility.

        Returns:
            A draw with stem and branch selections for the four pillars.

        Raises:
            ValidationError: If required birth data or options are invalid.
            EphemerisError: If the configured ephemeris cannot compute solar
                terms.
        """

        del rng
        birth = parse_birth_data(request, self.luck_count)
        time_model = (
            birth.time_model
            if "time_model" in (request.options or {})
            or (request.querent and "time_model" in (request.querent.attributes or {}))
            else self.time_model
        )
        day_boundary = (
            birth.day_boundary
            if "day_boundary" in (request.options or {})
            or (request.querent and "day_boundary" in (request.querent.attributes or {}))
            else self.day_boundary
        )
        effective = effective_datetime(
            birth.birth_datetime, birth.longitude, time_model, self.ephemeris
        )
        pillars = compute_pillars(
            birth.birth_datetime, effective, self.ephemeris, birth.gender, day_boundary
        )
        return draw_from_pillars(pillars, birth)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute Four Pillars without a caller RNG.

        Args:
            request: Reading request containing birth data and optional BaZi
                configuration.

        Returns:
            A reading with pillar placements and BaZi summary text.

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
        birth = parse_birth_data(request, self.luck_count)
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            f"time_model={birth.time_model.value}",
            f"day_boundary={birth.day_boundary.value}",
            "year_epoch=1984-jia-zi",
            "day_epoch=1984-02-02-jia-zi",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _summary_from_draw(draw: Draw) -> str:
    stem_indices: list[int] = []
    branch_indices: list[int] = []
    day_modifiers: dict[str, str] = {}
    for selection in draw.selections:
        modifiers = selection.modifiers or {}
        cycle_index = int(modifiers["cycle_index"])
        if modifiers.get("kind") == "stem":
            stem_indices.append(cycle_index % 10)
        else:
            branch_indices.append(cycle_index % 12)
        if selection.position_id == "day_stem":
            day_modifiers = dict(modifiers)
    distribution = element_distribution(tuple(stem_indices), tuple(branch_indices))
    strength = day_master_strength(stem_indices[2], tuple(branch_indices))
    month_index = int(day_modifiers["month_cycle_index"])
    forward = day_modifiers["luck_direction"] == "forward"
    start_age = float(day_modifiers["luck_start_age"])
    luck_count = int(day_modifiers["luck_count"])
    target_year = int(day_modifiers["target_year"])
    luck = luck_pillars(month_index, forward=forward, start_age=start_age, count=luck_count)
    luck_text = ", ".join(f"{pillar.cjk}@{pillar.start_age:.1f}" for pillar in luck)
    elements = ", ".join(f"{key}:{value}" for key, value in sorted(distribution.items()))
    return (
        f"Element distribution: {elements}. Day Master strength: {strength}. "
        f"Luck direction: {day_modifiers['luck_direction']}; Luck Pillars: {luck_text}. "
        f"Annual pillar {target_year}: {annual_pillar_cjk(target_year)}."
    )


def build_engine(
    ephemeris: Ephemeris | None = None,
    *,
    time_model: TimeModel = TimeModel.CLOCK,
    day_boundary: DayBoundary = DayBoundary.MIDNIGHT,
    luck_count: int = 8,
) -> FourPillarsEngine:
    """Create a Four Pillars engine.

    Args:
        ephemeris: Optional ephemeris backend. Defaults to the built-in
            pure-Python backend.
        time_model: Default time adjustment model.
        day_boundary: Default day-boundary rule.
        luck_count: Default number of Luck Pillars to render.

    Returns:
        A new ``FourPillarsEngine`` instance.
    """

    return FourPillarsEngine(
        ephemeris=ephemeris,
        time_model=time_model,
        day_boundary=day_boundary,
        luck_count=luck_count,
    )
