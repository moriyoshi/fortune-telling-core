"""Domino divination engine."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.dominoes.deck import DOMINOES_DECK
from fortune_telling_core.traditions.dominoes.spreads import SINGLE_TILE, THREE_TILES

_SPREADS = {spread.id: spread for spread in (SINGLE_TILE, THREE_TILES)}


class DominoesEngine(AbstractEngine):
    """Domino divination engine.

    The engine shuffles the 28-tile double-six set and draws into a single-tile
    or three-tile spread. Tiles carry no orientation.
    """

    id = "dominoes.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the domino deck for a request.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``DOMINOES_DECK.id``.

        Returns:
            The bundled domino deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != DOMINOES_DECK.id:
            raise ValidationError(f"unsupported domino deck: {request.deck_id}")
        return DOMINOES_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the domino spread requested by id.

        Args:
            request: Reading request whose ``spread_id`` selects a bundled
                spread.

        Returns:
            ``SINGLE_TILE`` or ``THREE_TILES``.

        Raises:
            ValidationError: If the spread is not supported.
        """

        spread = _SPREADS.get(request.spread_id)
        if spread is None:
            raise ValidationError(f"unsupported domino spread: {request.spread_id}")
        return spread

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Draw tiles for the requested spread.

        Args:
            request: Reading request.
            rng: Random source used to shuffle the set.

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


def build_engine() -> DominoesEngine:
    """Create a domino divination engine.

    Returns:
        A new ``DominoesEngine`` instance.
    """

    return DominoesEngine()
