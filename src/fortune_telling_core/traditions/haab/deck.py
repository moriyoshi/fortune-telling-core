"""Haab' deck: the eighteen winal and Wayeb'."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.haab.months import MONTHS

HAAB_DECK = Deck(
    id="haab.deck.months.v1",
    symbols=tuple(
        Symbol(
            id=month.symbol_id,
            name=month.name,
            attributes={
                "slug": month.slug,
                "cycle_index": str(month.index),
                "length": str(month.length),
            },
        )
        for month in MONTHS
    ),
)
