"""Rune deck: the twenty-four Elder Futhark runes."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.runes.runes import RUNES

RUNE_DECK = Deck(
    id="runes.deck.elder-futhark.v1",
    symbols=tuple(
        Symbol(
            id=rune.symbol_id,
            name=rune.name,
            attributes={
                "slug": rune.slug,
                "glyph": rune.glyph,
                "letter": rune.letter,
                "aett": rune.aett,
                "keyword": rune.keyword,
                "cycle_index": str(rune.index),
                "reversible": "true" if rune.reversible else "false",
            },
        )
        for rune in RUNES
    ),
)
