"""Tzolk'in engine."""

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
from fortune_telling_core.traditions.tzolkin.birth import parse_birth_data
from fortune_telling_core.traditions.tzolkin.chart import draw_from_day
from fortune_telling_core.traditions.tzolkin.daysigns import tzolkin_for
from fortune_telling_core.traditions.tzolkin.deck import TZOLKIN_DECK
from fortune_telling_core.traditions.tzolkin.spreads import TZOLKIN_SPREAD

_NULL_RNG = NullRng("TzolkinEngine.cast must not use randomness")


class TzolkinEngine(AbstractEngine):
    """Maya Tzolk'in (260-day sacred round) engine.

    The engine deterministically derives a querent's Tzolk'in day — a trecena
    number (1-13) paired with one of twenty day signs — from their birth date,
    using the GMT (584283) correlation anchored at 21 December 2012 = 4 Ajaw.
    """

    id = "tzolkin.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Tzolk'in day-sign deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``TZOLKIN_DECK.id``.

        Returns:
            The bundled Tzolk'in deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != TZOLKIN_DECK.id:
            raise ValidationError(f"unsupported Tzolk'in deck: {request.deck_id}")
        return TZOLKIN_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Tzolk'in spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``TZOLKIN_SPREAD.id``.

        Returns:
            The bundled Tzolk'in spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != TZOLKIN_SPREAD.id:
            raise ValidationError(f"unsupported Tzolk'in spread: {request.spread_id}")
        return TZOLKIN_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Tzolk'in day as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` in options or
                querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the single day-sign selection.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        del rng
        birth = parse_birth_data(request)
        return draw_from_day(tzolkin_for(birth.birth_datetime.date()))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Tzolk'in reading without a caller RNG.

        Args:
            request: Reading request containing birth data.

        Returns:
            A reading with the day-sign placement and Tzolk'in summary.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = (
            f"Tzolk'in day {modifiers['tzolkin']} "
            f"({modifiers['keyword']}, {modifiers['direction']})."
        )
        notes = tuple(base.provenance.notes) + (
            "correlation=gmt-584283",
            "anchor=2012-12-21-4-ajaw",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine() -> TzolkinEngine:
    """Create a Tzolk'in engine.

    Returns:
        A new ``TzolkinEngine`` instance.
    """

    return TzolkinEngine()
