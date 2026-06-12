"""Celtic tree chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.celtic_tree.deck import CELTIC_TREE_DECK
from fortune_telling_core.traditions.celtic_tree.signs import TreeSign
from fortune_telling_core.traditions.celtic_tree.spreads import CELTIC_TREE_SPREAD


def draw_from_sign(sign: TreeSign) -> Draw:
    selection = Selection(
        "tree_sign",
        sign.symbol_id,
        {
            "ogham": sign.ogham,
            "tree": sign.tree,
            "date_range": sign.date_range,
        },
    )
    return Draw(CELTIC_TREE_DECK.id, CELTIC_TREE_SPREAD.id, (selection,))
