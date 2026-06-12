"""Shared astronomical body identifiers."""

from enum import StrEnum


class Body(StrEnum):
    """Astronomical body identifiers accepted by shared ephemeris backends.

    Values are stable lowercase strings so they can be stored in reading
    modifiers and replay fixtures.

    Example:
        ```python
        from fortune_telling_core.astronomy import Body

        assert Body.SUN.value == "sun"
        ```
    """

    SUN = "sun"
    MOON = "moon"
    MERCURY = "mercury"
    VENUS = "venus"
    MARS = "mars"
    JUPITER = "jupiter"
    SATURN = "saturn"
    URANUS = "uranus"
    NEPTUNE = "neptune"
    PLUTO = "pluto"
    NORTH_NODE = "north_node"
    SOUTH_NODE = "south_node"
