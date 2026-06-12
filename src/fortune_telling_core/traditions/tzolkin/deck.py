"""Tzolk'in deck: the twenty day signs."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.tzolkin.daysigns import DAYSIGNS

TZOLKIN_DECK = Deck(
    id="tzolkin.deck.daysigns.v1",
    symbols=tuple(
        Symbol(
            id=sign.symbol_id,
            name=sign.name,
            attributes={
                "slug": sign.slug,
                "cycle_index": str(sign.index),
                "keyword": sign.keyword,
                "direction": sign.direction,
            },
        )
        for sign in DAYSIGNS
    ),
)
