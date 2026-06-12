"""Domino spreads as generic Spread data."""

from fortune_telling_core.spread import Position, Spread

SINGLE_TILE = Spread(
    id="dominoes.spread.single.v1",
    name="Single Tile",
    positions=(Position("tile", "Tile", "The drawn tile answering the question."),),
)

THREE_TILES = Spread(
    id="dominoes.spread.three.v1",
    name="Three Tiles",
    positions=(
        Position("past", "Past", "The relevant background."),
        Position("present", "Present", "The current influence."),
        Position("future", "Future", "The likely direction."),
    ),
)
