"""Numerology engine."""

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
from fortune_telling_core.traditions.numerology.birth import parse_birth_data
from fortune_telling_core.traditions.numerology.chart import draw_from_chart
from fortune_telling_core.traditions.numerology.config import ReductionMethod
from fortune_telling_core.traditions.numerology.deck import NUMEROLOGY_DECK
from fortune_telling_core.traditions.numerology.numbers import compute_chart
from fortune_telling_core.traditions.numerology.spreads import NUMEROLOGY_SPREAD

_NULL_RNG = NullRng("NumerologyEngine.cast must not use randomness")


class NumerologyEngine(AbstractEngine):
    """Pythagorean numerology engine.

    The engine deterministically reduces a querent's birth date to a Life Path
    number and a Birthday number, preserving the master numbers 11, 22, and 33.

    Args:
        reduction_method: Default Life Path reduction rule used when the request
            does not specify ``reduction_method``.
    """

    id = "numerology.engine"
    version = "0.1.0"

    def __init__(self, *, reduction_method: ReductionMethod = ReductionMethod.COMPONENT) -> None:
        self.reduction_method = reduction_method

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the numerology number deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``NUMEROLOGY_DECK.id``.

        Returns:
            The bundled numerology deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != NUMEROLOGY_DECK.id:
            raise ValidationError(f"unsupported numerology deck: {request.deck_id}")
        return NUMEROLOGY_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the numerology spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``NUMEROLOGY_SPREAD.id``.

        Returns:
            The bundled numerology spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != NUMEROLOGY_SPREAD.id:
            raise ValidationError(f"unsupported numerology spread: {request.spread_id}")
        return NUMEROLOGY_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the numerology numbers as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` and optional
                ``reduction_method`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the Life Path and Birthday selections.

        Raises:
            ValidationError: If required birth data or options are invalid.
        """

        del rng
        birth = parse_birth_data(request, self.reduction_method)
        return draw_from_chart(compute_chart(birth.birth_datetime.date(), birth.method))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a numerology reading without a caller RNG.

        Args:
            request: Reading request containing birth data and optional
                configuration.

        Returns:
            A reading with Life Path and Birthday placements and summary text.

        Raises:
            ValidationError: If required birth data or options are invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        life = dict(draw.selections[0].modifiers or {})
        birthday = dict(draw.selections[1].modifiers or {})
        summary = (
            f"Life Path {life['value']} ({life['keyword']}); "
            f"Birthday {birthday['value']} ({birthday['keyword']})."
        )
        notes = tuple(base.provenance.notes) + (
            f"reduction_method={life.get('reduction_method', self.reduction_method.value)}",
            "master_numbers=11-22-33",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine(
    *, reduction_method: ReductionMethod = ReductionMethod.COMPONENT
) -> NumerologyEngine:
    """Create a numerology engine.

    Args:
        reduction_method: Default Life Path reduction rule.

    Returns:
        A new ``NumerologyEngine`` instance.
    """

    return NumerologyEngine(reduction_method=reduction_method)
