"""Haab' spread."""

from fortune_telling_core.spread import Position, Spread

HAAB_SPREAD = Spread(
    id="haab.spread.birth.v1",
    name="Haab'",
    positions=(Position("haab", "Haab'", "Haab' month with the day position within it."),),
)
