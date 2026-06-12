"""Name numerology spread."""

from fortune_telling_core.spread import Position, Spread

NAME_NUMEROLOGY_SPREAD = Spread(
    id="name_numerology.spread.core.v1",
    name="Name Numbers",
    positions=(
        Position("expression", "Expression", "Destiny number from all letters."),
        Position("soul_urge", "Soul Urge", "Heart's desire number from the vowels."),
        Position("personality", "Personality", "Outer number from the consonants."),
    ),
)
