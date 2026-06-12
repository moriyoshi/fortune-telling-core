"""Elder Futhark rune-casting engine."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.runes.deck import RUNE_DECK
from fortune_telling_core.traditions.runes.spreads import NORNS, SINGLE_RUNE


class RuneEngine(AbstractEngine):
    """Elder Futhark rune-casting engine.

    The engine draws from the bundled 24-rune deck into a single-rune or Norns
    (past/present/future) spread, with optional reversals through the request
    option ``allow_reversals=true``. The eight symmetrical runes have no
    reversed form and are always cast upright, even when reversals are enabled.
    """

    id = "runes.elder-futhark.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Elder Futhark deck for a request.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``RUNE_DECK.id``.

        Returns:
            The bundled rune deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != RUNE_DECK.id:
            raise ValidationError(f"unsupported rune deck: {request.deck_id}")
        return RUNE_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the rune spread requested by id.

        Args:
            request: Reading request whose ``spread_id`` selects a bundled
                rune spread.

        Returns:
            ``SINGLE_RUNE`` or ``NORNS``.

        Raises:
            ValidationError: If the spread is not supported.
        """

        if request.spread_id == SINGLE_RUNE.id:
            return SINGLE_RUNE
        if request.spread_id == NORNS.id:
            return NORNS
        raise ValidationError(f"unsupported rune spread: {request.spread_id}")

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Cast runes for the requested spread.

        Args:
            request: Reading request. Set ``options={"allow_reversals":
                "true"}`` to include orientation modifiers.
            rng: Random source used to shuffle the deck and choose reversals.

        Returns:
            A draw containing one selection per spread position.

        Raises:
            ValidationError: If the requested deck or spread is unsupported.
            ExhaustedRngError: If the supplied RNG cannot provide enough values.
        """

        deck = self.deck(request)
        spread = self.spread(request)
        order = rng.shuffle(len(deck.symbols))
        allow_reversals = (
            request.options.get("allow_reversals") == "true" if request.options else False
        )

        selections: list[Selection] = []
        for position, symbol_index in zip(spread.positions, order[: spread.size], strict=True):
            symbol = deck.symbols[symbol_index]
            modifiers: dict[str, str] = {}
            if allow_reversals:
                # Consume one float per position so the stream stays aligned,
                # but only invertible runes can actually take a reversed form.
                turned = rng.random() < 0.5
                reversible = symbol.attributes.get("reversible") == "true"
                modifiers["orientation"] = "reversed" if turned and reversible else "upright"
            selections.append(
                Selection(
                    position_id=position.id,
                    symbol_id=symbol.id,
                    modifiers=modifiers,
                )
            )

        return Draw(deck_id=deck.id, spread_id=spread.id, selections=tuple(selections))


def build_engine() -> RuneEngine:
    """Create an Elder Futhark rune engine.

    Returns:
        A new ``RuneEngine`` instance.
    """

    return RuneEngine()
