"""Tarot reference engine."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.tarot.cards import RWS_DECK
from fortune_telling_core.traditions.tarot.spreads import SINGLE_CARD, THREE_CARD


class TarotEngine(AbstractEngine):
    """Reference Rider-Waite-Smith tarot engine.

    The engine supports the bundled Rider-Waite-Smith deck, single-card and
    three-card spreads, and optional reversals through the request option
    ``allow_reversals=true``.
    """

    id = "tarot.rws.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Rider-Waite-Smith deck for a request.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``RWS_DECK.id``.

        Returns:
            The bundled Rider-Waite-Smith deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != RWS_DECK.id:
            raise ValidationError(f"unsupported tarot deck: {request.deck_id}")
        return RWS_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the tarot spread requested by id.

        Args:
            request: Reading request whose ``spread_id`` selects a bundled
                tarot spread.

        Returns:
            ``SINGLE_CARD`` or ``THREE_CARD``.

        Raises:
            ValidationError: If the spread is not supported.
        """

        if request.spread_id == SINGLE_CARD.id:
            return SINGLE_CARD
        if request.spread_id == THREE_CARD.id:
            return THREE_CARD
        raise ValidationError(f"unsupported tarot spread: {request.spread_id}")

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Draw cards for the requested tarot spread.

        Args:
            request: Reading request. Set ``options={"allow_reversals":
                "true"}`` to include orientation modifiers.
            rng: Random source used to shuffle the deck and choose reversals.

        Returns:
            A draw containing one selection per spread position.

        Raises:
            ValidationError: If the requested deck or spread is unsupported.
            ExhaustedRngError: If the supplied RNG cannot provide enough
                values.
        """

        deck = self.deck(request)
        spread = self.spread(request)
        order = rng.shuffle(len(deck.symbols))
        allow_reversals = (
            request.options.get("allow_reversals") == "true" if request.options else False
        )

        selections: list[Selection] = []
        for position, symbol_index in zip(spread.positions, order[: spread.size], strict=True):
            modifiers: dict[str, str] = {}
            if allow_reversals:
                modifiers["orientation"] = "reversed" if rng.random() < 0.5 else "upright"
            selections.append(
                Selection(
                    position_id=position.id,
                    symbol_id=deck.symbols[symbol_index].id,
                    modifiers=modifiers,
                )
            )

        return Draw(deck_id=deck.id, spread_id=spread.id, selections=tuple(selections))


def build_engine() -> TarotEngine:
    """Create a Rider-Waite-Smith tarot engine.

    Returns:
        A new ``TarotEngine`` instance.

    Example:
        ```python
        from fortune_telling_core.traditions.tarot import build_engine

        engine = build_engine()
        ```
    """

    return TarotEngine()
