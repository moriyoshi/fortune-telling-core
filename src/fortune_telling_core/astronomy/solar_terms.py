"""Shared sectional solar-term helpers."""

from __future__ import annotations

from datetime import UTC, datetime

from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.solar import solar_longitude_crossing, sun_longitude

JIE_LONGITUDES: tuple[float, ...] = (
    315.0,
    345.0,
    15.0,
    45.0,
    75.0,
    105.0,
    135.0,
    165.0,
    195.0,
    225.0,
    255.0,
    285.0,
)


def solar_month_index(solar_longitude: float) -> int:
    """Return the sectional solar month index for a longitude.

    Args:
        solar_longitude: Apparent solar longitude in degrees.

    Returns:
        Zero-based index where 0 begins at Lichun, 315 degrees.
    """

    return int(((solar_longitude - 315.0) % 360.0) // 30.0)


def adjacent_jie_crossing(jd_tt: float, ephemeris: Ephemeris, *, forward: bool) -> float:
    """Find the previous or next sectional solar-term crossing.

    Args:
        jd_tt: Julian day on the Terrestrial Time scale.
        ephemeris: Ephemeris backend used for solar positions.
        forward: If true, find the next jie. Otherwise find the previous jie.

    Returns:
        Julian day of the adjacent sectional solar-term crossing.

    Raises:
        ValueError: If no crossing is found in the fixed 40-day bracket.
        EphemerisError: If the backend cannot compute the Sun.
    """

    current = sun_longitude(jd_tt, ephemeris)
    current_month = solar_month_index(current)
    target_index = (current_month + (1 if forward else 0)) % 12
    target = JIE_LONGITUDES[target_index]
    if forward:
        return solar_term_crossing(target, jd_tt, jd_tt + 40.0, ephemeris)
    return solar_term_crossing(target, jd_tt - 40.0, jd_tt, ephemeris)


def lichun_crossing(year: int, ephemeris: Ephemeris) -> float:
    """Find the Lichun crossing for a Gregorian year.

    Args:
        year: Gregorian calendar year.
        ephemeris: Ephemeris backend used for solar positions.

    Returns:
        Julian day on the Terrestrial Time scale when the Sun crosses
        315 degrees.

    Raises:
        ValueError: If the crossing is not found in the built-in bracket.
        EphemerisError: If the backend cannot compute the Sun.
    """

    start = jd_tt_from_utc(julian_day_utc(datetime(year, 1, 20, tzinfo=UTC)))
    end = jd_tt_from_utc(julian_day_utc(datetime(year, 2, 20, tzinfo=UTC)))
    return solar_term_crossing(315.0, start, end, ephemeris)


def solar_term_crossing(
    target: float, jd_start: float, jd_end: float, ephemeris: Ephemeris
) -> float:
    """Find a solar-term crossing by scanning one-day brackets.

    Args:
        target: Target apparent solar longitude in degrees.
        jd_start: Start Julian day of the search interval.
        jd_end: End Julian day of the search interval.
        ephemeris: Ephemeris backend used for solar positions.

    Returns:
        Julian day of the first crossing found in the interval.

    Raises:
        ValueError: If the crossing is not found.
        EphemerisError: If the backend cannot compute the Sun.
    """

    step = 1.0
    low = jd_start
    while low < jd_end:
        high = min(low + step, jd_end)
        try:
            return solar_longitude_crossing(target, low, high, ephemeris)
        except ValueError:
            low = high
    raise ValueError("solar term crossing not found")
