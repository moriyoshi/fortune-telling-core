"""Numerology deck: the single digits and master numbers."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.numerology.numbers import NUMBERS

NUMEROLOGY_DECK = Deck(
    id="numerology.deck.numbers.v1",
    symbols=tuple(
        Symbol(
            id=item.symbol_id,
            name=str(item.value),
            attributes={
                "value": str(item.value),
                "keyword": item.keyword,
                "master": "true" if item.master else "false",
            },
        )
        for item in NUMBERS
    ),
)
