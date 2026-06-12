"""Julian day helpers."""

from __future__ import annotations

from datetime import UTC, datetime

from fortune_telling_core._time import ensure_aware


def julian_day_utc(value: datetime) -> float:
    """Convert an aware civil datetime to a UTC Julian day.

    Args:
        value: A timezone-aware datetime. Naive datetimes are rejected by the
            shared time coercion helper.

    Returns:
        The Julian day as a float, including the fractional day.

    Raises:
        ValidationError: If ``value`` is naive.
    """

    aware = ensure_aware(value, "birth_datetime").astimezone(UTC)
    year = aware.year
    month = aware.month
    day = (
        aware.day
        + (
            aware.hour
            + (aware.minute + (aware.second + aware.microsecond / 1_000_000.0) / 60.0) / 60.0
        )
        / 24.0
    )

    if month <= 2:
        year -= 1
        month += 12
    correction_a = year // 100
    correction_b = 2 - correction_a + correction_a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + correction_b - 1524.5


def julian_day_from_date(year: int, month: int, day: int) -> int:
    """Return the midnight Julian day number for a Gregorian date.

    Args:
        year: Gregorian calendar year.
        month: Gregorian calendar month, from 1 to 12.
        day: Gregorian day of month.

    Returns:
        The integer Julian day number for midnight UTC on the date.
    """

    if month <= 2:
        year -= 1
        month += 12
    correction_a = year // 100
    correction_b = 2 - correction_a + correction_a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + correction_b - 1524


def julian_centuries(jd: float) -> float:
    """Convert a Julian day to Julian centuries since J2000.0.

    Args:
        jd: Julian day in any compatible time scale.

    Returns:
        Centuries elapsed since Julian day 2451545.0.
    """

    return (jd - 2451545.0) / 36525.0
