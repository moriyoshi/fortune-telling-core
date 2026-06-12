"""Rune spreads as generic Spread data."""

from fortune_telling_core.spread import Position, Spread

SINGLE_RUNE = Spread(
    id="runes.spread.single.v1",
    name="Single Rune",
    positions=(Position("focus", "Focus", "The central message of the casting."),),
)

NORNS = Spread(
    id="runes.spread.norns.v1",
    name="Norns",
    positions=(
        Position("urdr", "Urðr", "That which has become: the past."),
        Position("verdandi", "Verðandi", "That which is becoming: the present."),
        Position("skuld", "Skuld", "That which shall be: the future."),
    ),
)
