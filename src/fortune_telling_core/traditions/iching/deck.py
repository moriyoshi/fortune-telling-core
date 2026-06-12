"""I Ching deck: the 64 hexagrams."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.iching.hexagrams import HEXAGRAMS

ICHING_DECK = Deck(
    id="iching.deck.hexagrams.v1",
    symbols=tuple(
        Symbol(
            id=hexagram.symbol_id,
            name=hexagram.pinyin,
            attributes={
                "number": str(hexagram.number),
                "pinyin": hexagram.pinyin,
                "english": hexagram.english,
                "glyph": hexagram.glyph,
                "lower_trigram": hexagram.lower,
                "upper_trigram": hexagram.upper,
                "binary": format(hexagram.binary, "06b"),
            },
        )
        for hexagram in HEXAGRAMS
    ),
)
