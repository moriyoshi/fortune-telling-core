"""Modern Cyrillic Pythagorean spread."""

from fortune_telling_core.spread import Position, Spread

CYRILLIC_PYTHAGOREAN_SPREAD = Spread(
    id="cyrillic_pythagorean.spread.name.v1",
    name="Cyrillic Pythagorean Name Number",
    positions=(Position("name_number", "Name Number", "Root number reduced from the name."),),
)
