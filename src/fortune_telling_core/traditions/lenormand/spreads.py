"""Lenormand spreads as generic Spread data."""

from fortune_telling_core.spread import Position, Spread

SINGLE_CARD = Spread(
    id="lenormand.spread.single.v1",
    name="Single Card",
    positions=(Position("focus", "Focus", "The card answering the question."),),
)

THREE_CARD = Spread(
    id="lenormand.spread.three.v1",
    name="Three Card Line",
    positions=(
        Position("left", "Left", "Background, modifying the centre."),
        Position("center", "Centre", "The heart of the matter."),
        Position("right", "Right", "Outcome, modifying the centre."),
    ),
)

# The Grand Tableau lays out the entire deck in a 4x9 (plus 8x4+4) grid; here it
# is modelled as 36 ordered positions consuming every card.
GRAND_TABLEAU = Spread(
    id="lenormand.spread.grand-tableau.v1",
    name="Grand Tableau",
    positions=tuple(
        Position(f"house_{index}", f"House {index}", f"Tableau position {index}.")
        for index in range(1, 37)
    ),
)
