"""Chaldean numerology spread."""

from fortune_telling_core.spread import Position, Spread

CHALDEAN_NUMEROLOGY_SPREAD = Spread(
    id="chaldean_numerology.spread.name.v1",
    name="Chaldean Name Number",
    positions=(Position("name_number", "Name Number", "Root number reduced from the name."),),
)
