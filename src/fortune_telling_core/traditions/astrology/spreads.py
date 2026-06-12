"""Astrology spreads."""

from fortune_telling_core.spread import Position, Spread
from fortune_telling_core.traditions.astrology.bodies import NATAL_POSITIONS, POSITION_NAMES

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
