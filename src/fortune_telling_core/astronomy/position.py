"""Shared ecliptic position helpers."""

from dataclasses import dataclass


def normalize_degrees(value: float) -> float:
    """Normalize an angle to the half-open range ``[0, 360)``.

    Args:
        value: Angle in degrees.

    Returns:
        The equivalent angle in degrees, from 0 inclusive to 360 exclusive.
    """

    result = value % 360.0
    if result < 0.0:
        result += 360.0
    return result


@dataclass(frozen=True, slots=True)
class EclipticPosition:
    """Geocentric ecliptic position returned by an ephemeris.

    Args:
        longitude: Ecliptic longitude in degrees. The stored value is
            normalized to ``[0, 360)``.
        speed: Longitude speed in degrees per day. Negative speed is treated
            as retrograde motion.
        latitude: Ecliptic latitude in degrees, when the ephemeris computes
            it. ``None`` means latitude is unavailable for that body/backend.

    Example:
        ```python
        from fortune_telling_core.astronomy import EclipticPosition

        mars = EclipticPosition(721.0, -0.2)
        assert mars.longitude == 1.0
        assert mars.retrograde
        ```
    """

    longitude: float
    speed: float = 0.0
    latitude: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "longitude", normalize_degrees(float(self.longitude)))
        object.__setattr__(self, "speed", float(self.speed))
        if self.latitude is not None:
            object.__setattr__(self, "latitude", float(self.latitude))

    @property
    def retrograde(self) -> bool:
        """Whether the longitude speed is negative."""

        return self.speed < 0.0
