"""Astrological body and angle identifiers."""

from enum import StrEnum

from fortune_telling_core.astronomy.bodies import Body


class Angle(StrEnum):
    ASCENDANT = "ascendant"
    MIDHEAVEN = "midheaven"


PLANETARY_BODIES: tuple[Body, ...] = (
    Body.SUN,
    Body.MOON,
    Body.MERCURY,
    Body.VENUS,
    Body.MARS,
    Body.JUPITER,
    Body.SATURN,
    Body.URANUS,
    Body.NEPTUNE,
    Body.PLUTO,
    Body.NORTH_NODE,
    Body.SOUTH_NODE,
)

NATAL_POSITIONS: tuple[str, ...] = tuple(body.value for body in PLANETARY_BODIES) + (
    Angle.ASCENDANT.value,
    Angle.MIDHEAVEN.value,
)

POSITION_NAMES: dict[str, str] = {
    Body.SUN.value: "Sun",
    Body.MOON.value: "Moon",
    Body.MERCURY.value: "Mercury",
    Body.VENUS.value: "Venus",
    Body.MARS.value: "Mars",
    Body.JUPITER.value: "Jupiter",
    Body.SATURN.value: "Saturn",
    Body.URANUS.value: "Uranus",
    Body.NEPTUNE.value: "Neptune",
    Body.PLUTO.value: "Pluto",
    Body.NORTH_NODE.value: "North Node",
    Body.SOUTH_NODE.value: "South Node",
    Angle.ASCENDANT.value: "Ascendant",
    Angle.MIDHEAVEN.value: "Midheaven",
}

__all__ = ["Angle", "Body", "NATAL_POSITIONS", "PLANETARY_BODIES", "POSITION_NAMES"]
