"""Name numerology deck: the single digits and master numbers.

Reuses the number meanings from the birth-date numerology tradition, under a
distinct deck id and symbol ids.
"""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.numerology.numbers import NUMBERS


def _symbol_id(value: int) -> str:
    return f"name_numerology.number.{value}"


NAME_NUMEROLOGY_DECK = Deck(
    id="name_numerology.deck.numbers.v1",
    symbols=tuple(
        Symbol(
            id=_symbol_id(item.value),
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
