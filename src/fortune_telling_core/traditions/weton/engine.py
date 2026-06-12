"""Weton engine."""

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
from fortune_telling_core.traditions.weton.birth import parse_birth_data
from fortune_telling_core.traditions.weton.calendar import compute_weton
from fortune_telling_core.traditions.weton.chart import draw_from_chart
from fortune_telling_core.traditions.weton.config import DayBoundary
from fortune_telling_core.traditions.weton.deck import WETON_DECK
from fortune_telling_core.traditions.weton.spreads import WETON_SPREAD

_NULL_RNG = NullRng("WetonEngine.cast must not use randomness")


class WetonEngine(AbstractEngine):
    """Javanese weton engine.

    The engine deterministically derives the saptawara (seven-day week) and
    pancawara (five-day pasaran) from a birth datetime, then records both with
    their neptu values and the combined weton neptu.

    Args:
        day_boundary: Default Javanese day-rollover rule used when the request
            does not specify ``day_boundary``.
    """

    id = "weton.engine"
    version = "0.1.0"

    def __init__(self, *, day_boundary: DayBoundary = DayBoundary.MIDNIGHT) -> None:
        self.day_boundary = day_boundary

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the weton deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``WETON_DECK.id``.

        Returns:
            The bundled weton deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != WETON_DECK.id:
            raise ValidationError(f"unsupported weton deck: {request.deck_id}")
        return WETON_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the weton spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``WETON_SPREAD.id``.

        Returns:
            The bundled weton spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != WETON_SPREAD.id:
            raise ValidationError(f"unsupported weton spread: {request.spread_id}")
        return WETON_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the weton as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` and optional
                ``day_boundary`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with saptawara and pancawara selections.

        Raises:
            ValidationError: If required birth data or options are invalid.
        """

        del rng
        birth = parse_birth_data(request, self.day_boundary)
        chart = compute_weton(birth.birth_datetime, birth.day_boundary)
        return draw_from_chart(chart, birth.day_boundary)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a weton reading without a caller RNG.

        Args:
            request: Reading request containing birth data and optional
                configuration.

        Returns:
            A reading with saptawara and pancawara placements and weton summary
            text.

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
            "pancawara_anchor=1945-08-17-jumat-legi",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _summary_from_draw(draw: Draw) -> str:
    saptawara = dict(draw.selections[0].modifiers or {})
    pancawara = dict(draw.selections[1].modifiers or {})
    return (
        f"Weton {saptawara['weton']}: neptu {saptawara['day_neptu']} + "
        f"{pancawara['pasaran_neptu']} = {saptawara['neptu']}."
    )


def build_engine(*, day_boundary: DayBoundary = DayBoundary.MIDNIGHT) -> WetonEngine:
    """Create a weton engine.

    Args:
        day_boundary: Default Javanese day-rollover rule.

    Returns:
        A new ``WetonEngine`` instance.
    """

    return WetonEngine(day_boundary=day_boundary)
