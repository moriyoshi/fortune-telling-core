"""Petit Lenormand engine."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.lenormand.cards import LENORMAND_DECK
from fortune_telling_core.traditions.lenormand.spreads import (
    GRAND_TABLEAU,
    SINGLE_CARD,
    THREE_CARD,
)

_SPREADS = {spread.id: spread for spread in (SINGLE_CARD, THREE_CARD, GRAND_TABLEAU)}


class LenormandEngine(AbstractEngine):
    """Petit Lenormand engine.

    The engine draws from the 36-card deck into a single-card, three-card line,
    or Grand Tableau spread. Lenormand cards are not read reversed, so draws
    carry no orientation; the Grand Tableau consumes the entire deck.
    """

    id = "lenormand.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Lenormand deck for a request.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``LENORMAND_DECK.id``.

        Returns:
            The bundled Lenormand deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != LENORMAND_DECK.id:
            raise ValidationError(f"unsupported Lenormand deck: {request.deck_id}")
        return LENORMAND_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Lenormand spread requested by id.

        Args:
            request: Reading request whose ``spread_id`` selects a bundled
                spread.

        Returns:
            ``SINGLE_CARD``, ``THREE_CARD``, or ``GRAND_TABLEAU``.

        Raises:
            ValidationError: If the spread is not supported.
        """

        spread = _SPREADS.get(request.spread_id)
        if spread is None:
            raise ValidationError(f"unsupported Lenormand spread: {request.spread_id}")
        return spread

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Draw cards for the requested spread.

        Args:
            request: Reading request.
            rng: Random source used to shuffle the deck.

        Returns:
            A draw containing one selection per spread position.

        Raises:
            ValidationError: If the requested deck or spread is unsupported.
            ExhaustedRngError: If the supplied RNG cannot provide enough values.
        """

        deck = self.deck(request)
        spread = self.spread(request)
        order = rng.shuffle(len(deck.symbols))
        selections = tuple(
            Selection(position_id=position.id, symbol_id=deck.symbols[symbol_index].id)
            for position, symbol_index in zip(spread.positions, order[: spread.size], strict=True)
        )
        return Draw(deck_id=deck.id, spread_id=spread.id, selections=selections)


def build_engine() -> LenormandEngine:
    """Create a Petit Lenormand engine.

    Returns:
        A new ``LenormandEngine`` instance.
    """

    return LenormandEngine()
