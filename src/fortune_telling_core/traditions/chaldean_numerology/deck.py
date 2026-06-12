"""Chaldean numerology deck: the nine planetary root numbers."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.chaldean_numerology.numbers import NUMBERS

CHALDEAN_NUMEROLOGY_DECK = Deck(
    id="chaldean_numerology.deck.numbers.v1",
    symbols=tuple(
        Symbol(
            id=item.symbol_id,
            name=str(item.value),
            attributes={"value": str(item.value), "planet": item.planet},
        )
        for item in NUMBERS
    ),
)
