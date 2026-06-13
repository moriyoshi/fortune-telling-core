"""Greek isopsephy spread: a single total position."""

from fortune_telling_core.spread import Position, Spread

GREEK_ISOPSEPHY_SPREAD = Spread(
    id="greek_isopsephy.spread.name.v1",
    name="Greek Isopsephy Total",
    positions=(Position("total", "Total", "The summed isopsephy value of the name."),),
)
