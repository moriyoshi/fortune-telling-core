"""Can Chi engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core.draw import Draw
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.can_chi.birth import parse_birth_data
from fortune_telling_core.traditions.can_chi.chart import draw_from_chart
from fortune_telling_core.traditions.can_chi.config import DayBoundary
from fortune_telling_core.traditions.can_chi.deck import CAN_CHI_DECK
from fortune_telling_core.traditions.can_chi.pillars import compute_chart
from fortune_telling_core.traditions.can_chi.spreads import CAN_CHI_SPREAD

_NULL_RNG = NullRng("CanChiEngine.cast must not use randomness")


class CanChiEngine(AbstractEngine):
    """Vietnamese Can Chi (Thiên Can - Địa Chi) day and hour pillar engine.

    The engine deterministically computes the sexagenary day and hour pillars
    from a birth datetime using pure calendar arithmetic — no ephemeris — and
    records each stem and branch with its element, polarity, and con giáp
    animal. It shares Four Pillars' day anchor, so the two agree on every day.

    The year pillar (tuổi con giáp) is intentionally omitted: it rolls over at
    Tết, the lunar new year, which this dependency-free engine cannot locate
    without a lunar calendar.

    Args:
        day_boundary: Default day-rollover rule used when the request does not
            specify ``day_boundary``.
    """

    id = "canchi.engine"
    version = "0.1.0"

    def __init__(self, *, day_boundary: DayBoundary = DayBoundary.MIDNIGHT) -> None:
        self.day_boundary = day_boundary

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Can Chi deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``CAN_CHI_DECK.id``.

        Returns:
            The bundled Can Chi deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != CAN_CHI_DECK.id:
            raise ValidationError(f"unsupported Can Chi deck: {request.deck_id}")
        return CAN_CHI_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Can Chi spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``CAN_CHI_SPREAD.id``.

        Returns:
            The bundled Can Chi spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != CAN_CHI_SPREAD.id:
            raise ValidationError(f"unsupported Can Chi spread: {request.spread_id}")
        return CAN_CHI_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the day and hour Can Chi pillars as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` and optional
                ``day_boundary`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with day and hour stem/branch selections.

        Raises:
            ValidationError: If required birth data or options are invalid.
        """

        del rng
        birth = parse_birth_data(request, self.day_boundary)
        chart = compute_chart(birth.birth_datetime, birth.day_boundary)
        return draw_from_chart(chart, birth.day_boundary)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Can Chi reading without a caller RNG.

        Args:
            request: Reading request containing birth data and optional
                configuration.

        Returns:
            A reading with day and hour pillar placements and summary text.

        Raises:
            ValidationError: If required birth data or options are invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        summary = _summary_from_draw(draw)
        modifiers = dict(draw.selections[0].modifiers or {})
        notes = tuple(base.provenance.notes) + (
            f"day_boundary={modifiers.get('day_boundary', self.day_boundary.value)}",
            "day_anchor=2000-01-07-giap-ty",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _summary_from_draw(draw: Draw) -> str:
    common = dict(draw.selections[0].modifiers or {})
    day_animal = dict(draw.selections[1].modifiers or {})["animal"]
    hour_animal = dict(draw.selections[3].modifiers or {})["animal"]
    return (
        f"Day pillar {common['day_pillar']} ({day_animal}). "
        f"Hour pillar {common['hour_pillar']} ({hour_animal})."
    )


def build_engine(*, day_boundary: DayBoundary = DayBoundary.MIDNIGHT) -> CanChiEngine:
    """Create a Can Chi engine.

    Args:
        day_boundary: Default day-rollover rule.

    Returns:
        A new ``CanChiEngine`` instance.
    """

    return CanChiEngine(day_boundary=day_boundary)
