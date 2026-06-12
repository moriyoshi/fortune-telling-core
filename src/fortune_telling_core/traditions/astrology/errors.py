"""Astrology-specific errors."""

from fortune_telling_core.astronomy.errors import EphemerisError
from fortune_telling_core.errors import FortuneTellingError


class AstrologyError(FortuneTellingError):
    """Base astrology error."""


class PlacidusUndefinedError(AstrologyError):
    """Raised when Placidus houses are undefined for the requested latitude."""


__all__ = ["AstrologyError", "EphemerisError", "PlacidusUndefinedError"]
