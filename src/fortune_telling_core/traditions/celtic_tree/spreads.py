"""Celtic tree spread."""

from fortune_telling_core.spread import Position, Spread

CELTIC_TREE_SPREAD = Spread(
    id="celtic_tree.spread.birth.v1",
    name="Celtic Tree",
    positions=(Position("tree_sign", "Tree Sign", "Ogham tree sign for the birth date."),),
)
