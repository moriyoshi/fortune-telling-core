"""Weton configuration enums."""

from enum import StrEnum


class DayBoundary(StrEnum):
    """When the Javanese day (and therefore the weton) rolls over.

    The Javanese day traditionally begins at sunset rather than at midnight, so
    an evening birth can belong to the following weton. Sunset times depend on
    location, so this dependency-free engine approximates the sunset boundary
    with a fixed local-clock threshold of 18:00.
    """

    MIDNIGHT = "midnight"
    SUNSET = "sunset"


__all__ = ["DayBoundary"]
