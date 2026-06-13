"""Old Cyrillic numerals spread: a single total position."""

from fortune_telling_core.spread import Position, Spread

CYRILLIC_SLAVONIC_NUMERALS_SPREAD = Spread(
    id="cyrillic_slavonic_numerals.spread.name.v1",
    name="Old Cyrillic Numeral Total",
    positions=(Position("total", "Total", "The summed Old Cyrillic numeral value."),),
)
