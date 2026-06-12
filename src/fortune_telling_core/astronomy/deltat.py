"""Delta-T approximation."""


def delta_t_seconds(year: float) -> float:
    """Approximate Delta-T for a decimal year.

    Args:
        year: Decimal Gregorian year.

    Returns:
        Approximate ``TT - UT`` in seconds.
    """

    if year < 948.0:
        u = (year - 2000.0) / 100.0
        return 2177.0 + 497.0 * u + 44.1 * u * u
    if year < 1600.0:
        u = (year - 2000.0) / 100.0
        return 102.0 + 102.0 * u + 25.3 * u * u
    if year < 2000.0:
        t = year - 2000.0
        return 63.86 + 0.3345 * t - 0.060374 * t * t + 0.0017275 * t**3 + 0.000651814 * t**4
    if year < 2050.0:
        t = year - 2000.0
        return 62.92 + 0.32217 * t + 0.005589 * t * t
    u = (year - 1820.0) / 100.0
    return -20.0 + 32.0 * u * u


def jd_tt_from_utc(jd_utc: float) -> float:
    """Convert a UTC Julian day to Terrestrial Time.

    Args:
        jd_utc: Julian day on the UTC/UT scale.

    Returns:
        Julian day adjusted by the built-in Delta-T approximation.
    """

    year = 2000.0 + (jd_utc - 2451545.0) / 365.2425
    return jd_utc + delta_t_seconds(year) / 86400.0
