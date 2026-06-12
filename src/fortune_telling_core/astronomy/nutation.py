"""Small nutation and obliquity helpers."""

import math

from fortune_telling_core.astronomy.julian import julian_centuries


def mean_obliquity(jd_tt: float) -> float:
    """Return the mean obliquity of the ecliptic.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.

    Returns:
        Mean obliquity in degrees.
    """

    t = julian_centuries(jd_tt)
    seconds = 21.448 - t * (46.8150 + t * (0.00059 - t * 0.001813))
    return 23.0 + (26.0 + seconds / 60.0) / 60.0


def nutation_longitude(jd_tt: float) -> float:
    """Return the nutation in ecliptic longitude.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.

    Returns:
        Nutation longitude correction in degrees.
    """

    t = julian_centuries(jd_tt)
    omega = math.radians(125.04452 - 1934.136261 * t)
    sun_mean = math.radians(280.4665 + 36000.7698 * t)
    moon_mean = math.radians(218.3165 + 481267.8813 * t)
    seconds = (
        -17.20 * math.sin(omega)
        - 1.32 * math.sin(2.0 * sun_mean)
        - 0.23 * math.sin(2.0 * moon_mean)
        + 0.21 * math.sin(2.0 * omega)
    )
    return seconds / 3600.0


def true_obliquity(jd_tt: float) -> float:
    """Return the true obliquity of the ecliptic.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.

    Returns:
        True obliquity in degrees.
    """

    t = julian_centuries(jd_tt)
    omega = math.radians(125.04452 - 1934.136261 * t)
    delta_eps_seconds = 9.20 * math.cos(omega)
    return mean_obliquity(jd_tt) + delta_eps_seconds / 3600.0
