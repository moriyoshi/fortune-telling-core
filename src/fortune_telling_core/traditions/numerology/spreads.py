"""Numerology spread."""

from fortune_telling_core.spread import Position, Spread

NUMEROLOGY_SPREAD = Spread(
    id="numerology.spread.birth.v1",
    name="Numerology",
    positions=(
        Position("life_path", "Life Path", "Core number reduced from the full birth date."),
        Position("birthday", "Birthday", "Number reduced from the day of the month."),
    ),
)
