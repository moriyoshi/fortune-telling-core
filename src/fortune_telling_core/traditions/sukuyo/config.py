"""Sukuyō configuration enums."""

from enum import StrEnum


class Ayanamsa(StrEnum):
    """Sidereal zero-point (ayanamsa) used to derive the birth mansion.

    The 27 mansions are equal 13°20′ sidereal divisions, so the ayanamsa fixes
    which mansion a Moon longitude falls in. ``LAHIRI`` is the default and the
    most common choice for nakshatra-derived systems. ``FAGAN_BRADLEY`` is the
    Western sidereal standard. ``NONE`` keeps tropical longitudes (no
    correction), mainly for testing and comparison.

    Both non-zero ayanamsas use the same precession rate and differ only by a
    fixed epoch offset; they are documented linear approximations adequate for
    mansion determination, not high-precision astrology.
    """

    LAHIRI = "lahiri"
    FAGAN_BRADLEY = "fagan_bradley"
    NONE = "none"


class Method(StrEnum):
    """Birth-mansion determination method.

    ``MOON_LONGITUDE`` derives the mansion from the Moon's sidereal ecliptic
    longitude at birth using the bundled ephemeris. The traditional
    lunisolar-table (月宿傍通暦) method is not bundled; it can be added here as a
    future value.
    """

    MOON_LONGITUDE = "moon_longitude"


__all__ = ["Ayanamsa", "Method"]
