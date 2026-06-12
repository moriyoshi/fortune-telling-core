"""Shared astronomy errors."""

from fortune_telling_core.errors import FortuneTellingError


class AstronomyError(FortuneTellingError):
    """Base error for shared astronomy helpers."""


class EphemerisError(AstronomyError):
    """Raised when an ephemeris cannot provide a requested position."""
