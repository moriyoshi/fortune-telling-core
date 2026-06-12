"""Tarot reference spreads as generic Spread data."""

from fortune_telling_core.spread import Position, Spread

SINGLE_CARD = Spread(
    id="tarot.spread.single.v1",
    name="Single Card",
    positions=(
        Position(
            id="focus",
            name="Focus",
            description="The central message for the reading.",
        ),
    ),
)

THREE_CARD = Spread(
    id="tarot.spread.three-card.v1",
    name="Past, Present, Future",
    positions=(
        Position(id="past", name="Past", description="The relevant background."),
        Position(id="present", name="Present", description="The current influence."),
        Position(id="future", name="Future", description="The likely direction."),
    ),
)
