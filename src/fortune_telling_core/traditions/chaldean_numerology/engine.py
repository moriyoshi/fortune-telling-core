"""Chaldean numerology engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions._name_text import format_value_trace
from fortune_telling_core.traditions._name_values import latin_chaldean
from fortune_telling_core.traditions.chaldean_numerology.deck import CHALDEAN_NUMEROLOGY_DECK
from fortune_telling_core.traditions.chaldean_numerology.numbers import (
    compute_name_number,
    number,
)
from fortune_telling_core.traditions.chaldean_numerology.spreads import (
    CHALDEAN_NUMEROLOGY_SPREAD,
)

_NULL_RNG = NullRng("ChaldeanNumerologyEngine.cast must not use randomness")


class ChaldeanNumerologyEngine(AbstractEngine):
    """Chaldean numerology engine.

    The engine deterministically reduces a name to its Chaldean root number
    (1-9) and surfaces the planetary ruler of that root.
    """

    id = "chaldean_numerology.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Chaldean numerology deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``CHALDEAN_NUMEROLOGY_DECK.id``.

        Returns:
            The bundled deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != CHALDEAN_NUMEROLOGY_DECK.id:
            raise ValidationError(f"unsupported Chaldean numerology deck: {request.deck_id}")
        return CHALDEAN_NUMEROLOGY_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Chaldean numerology spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``CHALDEAN_NUMEROLOGY_SPREAD.id``.

        Returns:
            The bundled spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != CHALDEAN_NUMEROLOGY_SPREAD.id:
            raise ValidationError(f"unsupported Chaldean numerology spread: {request.spread_id}")
        return CHALDEAN_NUMEROLOGY_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Chaldean name number as a deterministic draw.

        Args:
            request: Reading request with ``name`` in options or querent
                attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the single name-number selection.

        Raises:
            ValidationError: If the name is missing or invalid.
        """

        del rng
        name = require_string(collect_values(request), "name")
        units = latin_chaldean.values(name)
        result = compute_name_number(name)
        data = number(result.root)
        selection = Selection(
            "name_number",
            data.symbol_id,
            {
                "value": str(data.value),
                "planet": data.planet,
                "total": str(result.total),
                "value_system": latin_chaldean.ID,
                "value_system_version": latin_chaldean.VERSION,
                "normalization": "latin_ascii_ignore",
                "normalized_name": "".join(unit.char for unit in units),
                "values": format_value_trace(units),
            },
        )
        return Draw(CHALDEAN_NUMEROLOGY_DECK.id, CHALDEAN_NUMEROLOGY_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Chaldean numerology reading without a caller RNG.

        Args:
            request: Reading request containing the name.

        Returns:
            A reading with the name-number placement and summary.

        Raises:
            ValidationError: If the name is missing or invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = (
            f"Name number {modifiers['value']} ({modifiers['planet']}); total {modifiers['total']}."
        )
        notes = tuple(base.provenance.notes) + (
            "system=chaldean",
            f"value_system={latin_chaldean.ID}",
            "normalization=latin_ascii_ignore",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine() -> ChaldeanNumerologyEngine:
    """Create a Chaldean numerology engine.

    Returns:
        A new ``ChaldeanNumerologyEngine`` instance.
    """

    return ChaldeanNumerologyEngine()
