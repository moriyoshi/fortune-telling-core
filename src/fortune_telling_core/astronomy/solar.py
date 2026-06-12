"""Solar helpers shared by deterministic traditions."""

import math

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.nutation import true_obliquity
from fortune_telling_core.astronomy.position import normalize_degrees


def sun_longitude(jd_tt: float, ephemeris: Ephemeris) -> float:
    """Return the Sun's apparent ecliptic longitude.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.
        ephemeris: Ephemeris backend used to compute the Sun's position.

    Returns:
        Apparent geocentric longitude in degrees.

    Raises:
        EphemerisError: If the backend does not support the Sun.
    """

    return ephemeris.position(Body.SUN, jd_tt).longitude


def wrap180(value: float) -> float:
    """Wrap an angle to ``[-180, 180)`` degrees.

    Args:
        value: Angle in degrees.

    Returns:
        The equivalent signed angle in degrees.
    """

    return (value + 180.0) % 360.0 - 180.0


def solar_longitude_crossing(
    target_deg: float,
    jd_start: float,
    jd_end: float,
    ephemeris: Ephemeris,
    *,
    tolerance_deg: float = 1e-6,
    max_iterations: int = 100,
) -> float:
    """Find when the Sun crosses a target longitude inside a bracket.

    Args:
        target_deg: Target apparent solar longitude in degrees.
        jd_start: Start of the Julian-day search bracket.
        jd_end: End of the Julian-day search bracket.
        ephemeris: Ephemeris backend used for solar positions.
        tolerance_deg: Maximum remaining longitude error before returning.
        max_iterations: Maximum bisection iterations.

    Returns:
        Julian day of the crossing.

    Raises:
        ValueError: If the target is not bracketed by the supplied interval.
        EphemerisError: If the backend cannot compute the Sun.
    """

    target = normalize_degrees(target_deg)
    low = jd_start
    high = jd_end
    low_value = wrap180(sun_longitude(low, ephemeris) - target)
    high_value = wrap180(sun_longitude(high, ephemeris) - target)
    if low_value == 0.0:
        return low
    if high_value == 0.0:
        return high
    if low_value * high_value > 0.0:
        raise ValueError("solar longitude target is not bracketed")
    for _ in range(max_iterations):
        mid = (low + high) / 2.0
        mid_value = wrap180(sun_longitude(mid, ephemeris) - target)
        if abs(mid_value) <= tolerance_deg:
            return mid
        if low_value * mid_value <= 0.0:
            high = mid
            high_value = mid_value
        else:
            low = mid
            low_value = mid_value
    return (low + high) / 2.0


def equation_of_time(jd_tt: float, ephemeris: Ephemeris) -> float:
    """Approximate the equation of time for a Julian day.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.
        ephemeris: Ephemeris backend used for the Sun's longitude.

    Returns:
        Apparent solar time minus mean solar time, in minutes.

    Raises:
        EphemerisError: If the backend cannot compute the Sun.
    """

    sun = math.radians(sun_longitude(jd_tt, ephemeris))
    eps = math.radians(true_obliquity(jd_tt))
    right_ascension = math.degrees(math.atan2(math.sin(sun) * math.cos(eps), math.cos(sun)))
    return wrap180(sun_longitude(jd_tt, ephemeris) - right_ascension) * 4.0
