"""Astrology spreads."""

from fortune_telling_core.spread import Position, Spread
from fortune_telling_core.traditions.astrology.bodies import NATAL_POSITIONS, POSITION_NAMES, Body

NATAL_CHART = Spread(
    id="astro.spread.natal.v1",
    name="Natal Chart",
    positions=tuple(
        Position(
            id=position_id,
            name=POSITION_NAMES[position_id],
            description=f"Natal placement for {POSITION_NAMES[position_id]}.",
        )
        for position_id in NATAL_POSITIONS
    ),
)

# The sun-sign reading is a single placement: the Sun's zodiac sign. It reuses
# the ``sun`` position id so the same Sun-in-sign interpretation data applies as
# in the natal chart. Unlike the natal chart it needs only a birth date (or an
# explicit sign), not a birth time or location.
SUN_SIGN = Spread(
    id="astro.spread.sun_sign.v1",
    name="Sun Sign",
    positions=(
        Position(
            id=Body.SUN.value,
            name="Sun Sign",
            description="Zodiac sun sign for the birth date.",
        ),
    ),
)
