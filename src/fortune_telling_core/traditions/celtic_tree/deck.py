"""Celtic tree deck: the thirteen Ogham tree signs."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.celtic_tree.signs import SIGNS

CELTIC_TREE_DECK = Deck(
    id="celtic_tree.deck.signs.v1",
    symbols=tuple(
        Symbol(
            id=sign.symbol_id,
            name=sign.tree,
            attributes={
                "slug": sign.slug,
                "ogham": sign.ogham,
                "tree": sign.tree,
                "cycle_index": str(sign.index),
                "date_range": sign.date_range,
            },
        )
        for sign in SIGNS
    ),
)
