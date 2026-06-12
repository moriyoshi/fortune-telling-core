"""Name numerology engine."""

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
from fortune_telling_core.traditions.name_numerology.chart import draw_from_chart
from fortune_telling_core.traditions.name_numerology.compute import compute_chart
from fortune_telling_core.traditions.name_numerology.config import YMode
from fortune_telling_core.traditions.name_numerology.deck import NAME_NUMEROLOGY_DECK
from fortune_telling_core.traditions.name_numerology.parse import parse_name_input
from fortune_telling_core.traditions.name_numerology.spreads import NAME_NUMEROLOGY_SPREAD

_NULL_RNG = NullRng("NameNumerologyEngine.cast must not use randomness")


class NameNumerologyEngine(AbstractEngine):
    """Pythagorean name numerology engine.

    The engine deterministically reduces a name to its Expression, Soul Urge,
    and Personality numbers, preserving the master numbers 11, 22, and 33.

    Args:
        y_mode: Default treatment of the letter Y when the request does not
            specify ``y_mode``.
    """

    id = "name_numerology.engine"
    version = "0.1.0"

    def __init__(self, *, y_mode: YMode = YMode.CONSONANT) -> None:
        self.y_mode = y_mode

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the name numerology deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``NAME_NUMEROLOGY_DECK.id``.

        Returns:
            The bundled deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != NAME_NUMEROLOGY_DECK.id:
            raise ValidationError(f"unsupported name numerology deck: {request.deck_id}")
        return NAME_NUMEROLOGY_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the name numerology spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``NAME_NUMEROLOGY_SPREAD.id``.

        Returns:
            The bundled spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != NAME_NUMEROLOGY_SPREAD.id:
            raise ValidationError(f"unsupported name numerology spread: {request.spread_id}")
        return NAME_NUMEROLOGY_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the core name numbers as a deterministic draw.

        Args:
            request: Reading request with ``name`` and optional ``y_mode`` in
                options or querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the Expression, Soul Urge, and Personality selections.

        Raises:
            ValidationError: If the name or options are invalid.
        """

        del rng
        name_input = parse_name_input(request, self.y_mode)
        return draw_from_chart(compute_chart(name_input.name, name_input.y_mode))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a name numerology reading without a caller RNG.

        Args:
            request: Reading request containing the name and optional
                configuration.

        Returns:
            A reading with the three core-number placements and summary.

        Raises:
            ValidationError: If the name or options are invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        expression = dict(draw.selections[0].modifiers or {})
        soul = dict(draw.selections[1].modifiers or {})
        personality = dict(draw.selections[2].modifiers or {})
        summary = (
            f"Expression {expression['value']} ({expression['keyword']}); "
            f"Soul Urge {soul['value']} ({soul['keyword']}); "
            f"Personality {personality['value']} ({personality['keyword']})."
        )
        notes = tuple(base.provenance.notes) + (
            f"y_mode={expression.get('y_mode', self.y_mode.value)}",
            "system=pythagorean",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine(*, y_mode: YMode = YMode.CONSONANT) -> NameNumerologyEngine:
    """Create a name numerology engine.

    Args:
        y_mode: Default treatment of the letter Y.

    Returns:
        A new ``NameNumerologyEngine`` instance.
    """

    return NameNumerologyEngine(y_mode=y_mode)
