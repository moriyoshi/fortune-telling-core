"""Lunisolar (旧暦) calendar conversion.

Converts a civil instant to a Japanese-style lunisolar date using the
定気法 (true-position) rules:

* Lunar months begin on the civil day of an astronomical new moon (朔).
* Month 11 is the lunar month containing the winter solstice (冬至, solar
  longitude 270°).
* When a winter-solstice-to-winter-solstice block (歳) holds 13 new moons, the
  first month with no principal term (中気) is the leap month (閏月) and takes
  the previous month's number.

The implementation is pure Python on top of the bundled ephemeris. Like every
true-position lunisolar scheme it is subject to the well-known 2033 problem,
where the leap-month placement is genuinely ambiguous; callers needing that
window should treat results there with care.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import delta_t_seconds, jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.solar import sun_longitude

_SYNODIC_MONTH = 29.530588853
# A known new moon near J2000: 2000-01-06 18:14 UTC.
_NEW_MOON_EPOCH_JD = 2451550.259722


@dataclass(frozen=True, slots=True)
class LunisolarDate:
    """A lunisolar (旧暦) date."""

    year: int
    month: int
    day: int
    is_leap_month: bool


def _moon_sun_elongation(jd_tt: float, ephemeris: Ephemeris) -> float:
    moon = ephemeris.position(Body.MOON, jd_tt).longitude
    sun = ephemeris.position(Body.SUN, jd_tt).longitude
    return (moon - sun) % 360.0


def _signed_elongation(jd_tt: float, ephemeris: Ephemeris) -> float:
    elongation = _moon_sun_elongation(jd_tt, ephemeris)
    return elongation - 360.0 if elongation > 180.0 else elongation


def _refine_new_moon(jd_guess: float, ephemeris: Ephemeris) -> float:
    """Newton-refine an approximate Julian day to a new-moon instant (TT)."""

    jd = jd_guess
    for _ in range(8):
        delta = _signed_elongation(jd, ephemeris)
        jd -= delta / 12.190749  # mean elongation rate, deg/day
    return jd


def new_moon_on_or_before(jd_tt: float, ephemeris: Ephemeris) -> float:
    """Return the Julian day (TT) of the last new moon at or before ``jd_tt``."""

    cycle = round((jd_tt - _NEW_MOON_EPOCH_JD) / _SYNODIC_MONTH)
    jd = _refine_new_moon(_NEW_MOON_EPOCH_JD + cycle * _SYNODIC_MONTH, ephemeris)
    while jd > jd_tt + 0.5:
        cycle -= 1
        jd = _refine_new_moon(_NEW_MOON_EPOCH_JD + cycle * _SYNODIC_MONTH, ephemeris)
    while True:
        nxt = _refine_new_moon(_NEW_MOON_EPOCH_JD + (cycle + 1) * _SYNODIC_MONTH, ephemeris)
        if nxt > jd_tt + 0.5:
            break
        cycle += 1
        jd = nxt
    return jd


def _year_of_jd(jd_tt: float) -> int:
    return int((jd_tt - 2451545.0) / 365.25) + 2000


def civil_day_number(jd_tt: float, tz_hours: float) -> int:
    """Return the integer civil day number of a TT Julian day in a timezone.

    The result is comparable with
    :func:`fortune_telling_core.astronomy.julian.julian_day_from_date` for the
    same local date.
    """

    delta_t_days = delta_t_seconds(_year_of_jd(jd_tt)) / 86400.0
    jd_ut = jd_tt - delta_t_days
    return math.floor(jd_ut + tz_hours / 24.0 + 0.5)


def _winter_solstice(year: int, ephemeris: Ephemeris) -> float:
    """Return the Julian day (TT) of the winter solstice (270°) of a year."""

    # Bracket early December to mid January and bisect on (lon - 270).
    start = jd_tt_from_utc(julian_day_utc(_utc(year, 12, 1)))
    end = jd_tt_from_utc(julian_day_utc(_utc(year + 1, 1, 15)))
    return _solar_crossing(270.0, start, end, ephemeris)


def _utc(year: int, month: int, day: int):  # type: ignore[no-untyped-def]
    from datetime import UTC, datetime

    return datetime(year, month, day, tzinfo=UTC)


def _wrap180(value: float) -> float:
    return (value + 180.0) % 360.0 - 180.0


def _solar_crossing(target: float, low: float, high: float, ephemeris: Ephemeris) -> float:
    low_value = _wrap180(sun_longitude(low, ephemeris) - target)
    for _ in range(100):
        mid = (low + high) / 2.0
        mid_value = _wrap180(sun_longitude(mid, ephemeris) - target)
        if abs(mid_value) <= 1e-7:
            return mid
        if low_value * mid_value <= 0.0:
            high = mid
        else:
            low, low_value = mid, mid_value
    return (low + high) / 2.0


def _has_principal_term(
    start_jd: float, end_jd: float, tz_hours: float, ephemeris: Ephemeris
) -> bool:
    """Whether a principal term (中気, multiple of 30°) falls in [start, end)."""

    start_day = civil_day_number(start_jd, tz_hours)
    end_day = civil_day_number(end_jd, tz_hours)
    lon = sun_longitude(start_jd, ephemeris)
    target = (math.ceil(lon / 30.0 - 1e-9) * 30.0) % 360.0
    crossing = _solar_crossing(target, start_jd, start_jd + 32.0, ephemeris)
    crossing_day = civil_day_number(crossing, tz_hours)
    return start_day <= crossing_day < end_day


def to_lunisolar(jd_tt: float, *, tz_hours: float, ephemeris: Ephemeris) -> LunisolarDate:
    """Convert a TT Julian day to a lunisolar (旧暦) date.

    Args:
        jd_tt: Instant to convert, as a Terrestrial-Time Julian day.
        tz_hours: Civil timezone offset (hours east of UTC) in which lunar
            day boundaries are taken. Japanese 旧暦 uses ``9.0``.
        ephemeris: Ephemeris backend for Sun and Moon positions.

    Returns:
        The lunisolar date.
    """

    target_day = civil_day_number(jd_tt, tz_hours)
    month_start = new_moon_on_or_before(jd_tt, ephemeris)
    gregorian_year = _year_of_jd(jd_tt)

    # Two candidate month-11 anchors (new moon starting the solstice month).
    anchor_prev = new_moon_on_or_before(_winter_solstice(gregorian_year - 1, ephemeris), ephemeris)
    anchor_this = new_moon_on_or_before(_winter_solstice(gregorian_year, ephemeris), ephemeris)

    if civil_day_number(month_start, tz_hours) >= civil_day_number(anchor_this, tz_hours):
        anchor = anchor_this
        anchor_year = gregorian_year
        next_anchor = new_moon_on_or_before(
            _winter_solstice(gregorian_year + 1, ephemeris), ephemeris
        )
    else:
        anchor = anchor_prev
        anchor_year = gregorian_year - 1
        next_anchor = anchor_this

    # Each month in this solstice block: its new-moon instant and civil day.
    months: list[int] = []
    month_jds: list[float] = []
    next_day = civil_day_number(next_anchor, tz_hours)
    nm = anchor
    while civil_day_number(nm, tz_hours) < next_day:
        month_jds.append(nm)
        months.append(civil_day_number(nm, tz_hours))
        nm = new_moon_on_or_before(nm + _SYNODIC_MONTH + 2.0, ephemeris)

    leap_index: int | None = None
    if len(months) == 13:
        for index in range(len(month_jds)):
            start = month_jds[index]
            end = month_jds[index + 1] if index + 1 < len(month_jds) else next_anchor
            if not _has_principal_term(start, end, tz_hours, ephemeris):
                leap_index = index
                break

    number = 11
    prev_number = 11
    numbers: list[int] = []
    leaps: list[bool] = []
    for index in range(len(months)):
        if index == leap_index:
            numbers.append(prev_number)
            leaps.append(True)
        else:
            numbers.append(number)
            leaps.append(False)
            prev_number = number
            number = number + 1 if number < 12 else 1

    target_index = 0
    for index in range(len(months)):
        if months[index] <= target_day:
            target_index = index
        else:
            break

    month_number = numbers[target_index]
    is_leap = leaps[target_index]
    day = target_day - months[target_index] + 1
    lunar_year = anchor_year if month_number >= 11 else anchor_year + 1
    return LunisolarDate(lunar_year, month_number, day, is_leap)


__all__ = [
    "LunisolarDate",
    "civil_day_number",
    "new_moon_on_or_before",
    "to_lunisolar",
]
