"""Nine Star Ki star calculations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_from_date, julian_day_utc
from fortune_telling_core.astronomy.solar import sun_longitude
from fortune_telling_core.astronomy.solar_terms import (
    lichun_crossing,
    solar_month_index,
    solar_term_crossing,
)
from fortune_telling_core.traditions.nine_star_ki.config import DayStarEscapement
from fortune_telling_core.traditions.nine_star_ki.lo_shu import fly_chart
from fortune_telling_core.traditions.nine_star_ki.stars import HOME_STAR_BY_PALACE

# 2000-01-07 is a Jia-Zi (甲子) day. Note: 1984-02-02 (this code's previous
# anchor) is NOT Jia-Zi — 万年暦 lookups place it at Bing-Yin / 丙寅, two days
# later in the cycle. 1984 is a Jia-Zi *year*, the likely source of the mix-up.
DAY_JIAZI_JDN = julian_day_from_date(2000, 1, 7)


@dataclass(frozen=True, slots=True)
class NineStarKiChart:
    solar_year: int
    year_star: int
    solar_month_index: int
    month_star: int
    day_star: int
    day_direction: str
    day_star_escapement: DayStarEscapement
    tendency_star: int
    center_case: bool
    target_year: int
    annual_star: int


def compute_chart(
    birth_datetime: datetime,
    effective_dt: datetime,
    ephemeris: Ephemeris,
    target_year: int,
    day_star_escapement: DayStarEscapement = DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE,
) -> NineStarKiChart:
    jd_tt = jd_tt_from_utc(julian_day_utc(birth_datetime))
    solar_year = solar_year_for_datetime(effective_dt, jd_tt, ephemeris)
    year = year_star(solar_year)
    month_index = solar_month_index(sun_longitude(jd_tt, ephemeris))
    month = month_star(year, month_index)
    day, direction = day_star(effective_dt, jd_tt, ephemeris, day_star_escapement)
    tendency, center_case = tendency_star(year, month)
    return NineStarKiChart(
        solar_year=solar_year,
        year_star=year,
        solar_month_index=month_index,
        month_star=month,
        day_star=day,
        day_direction=direction,
        day_star_escapement=day_star_escapement,
        tendency_star=tendency,
        center_case=center_case,
        target_year=target_year,
        annual_star=year_star(target_year),
    )


def solar_year_for_datetime(effective_dt: datetime, jd_tt: float, ephemeris: Ephemeris) -> int:
    local_year = effective_dt.year
    try:
        if jd_tt < lichun_crossing(local_year, ephemeris):
            return local_year - 1
    except ValueError:
        solar_lon = sun_longitude(jd_tt, ephemeris)
        if solar_lon < 315.0 and effective_dt.month <= 2:
            return local_year - 1
    return local_year


def year_star(solar_year: int) -> int:
    return _wrap_star(1 - (solar_year - 1900))


def year_star_digit_sum_oracle(solar_year: int) -> int:
    value = 11 - sum(int(digit) for digit in str(solar_year))
    while value <= 0:
        value += 9
    return _wrap_star(value)


def year_star_digit_root_oracle(solar_year: int) -> int:
    digit_root = 1 + ((sum(int(digit) for digit in str(solar_year)) - 1) % 9)
    return _wrap_star(11 - digit_root)


def month_star(principal_star: int, month_index: int) -> int:
    if principal_star in {1, 4, 7}:
        start = 8
    elif principal_star in {2, 5, 8}:
        start = 2
    else:
        start = 5
    return _wrap_star(start - month_index)


def day_star(
    effective_dt: datetime,
    jd_tt: float,
    ephemeris: Ephemeris,
    escapement: DayStarEscapement = DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE,
) -> tuple[int, str]:
    day_jdn = julian_day_from_date(
        effective_dt.date().year, effective_dt.date().month, effective_dt.date().day
    )
    forward, solstice_jd = _day_escapement(effective_dt.year, jd_tt, ephemeris)
    solstice_jdn = _solstice_jdn(solstice_jd)
    if escapement == DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE:
        anchor = _jiazi_at_or_before(solstice_jdn)
    elif escapement == DayStarEscapement.FIRST_JIAZI_AFTER_SOLSTICE:
        anchor = _jiazi_after(solstice_jdn)
    else:
        raise ValueError(f"unsupported day-star escapement: {escapement}")
    if forward:
        return _wrap_star(1 + day_jdn - anchor), "forward"
    return _wrap_star(9 - (day_jdn - anchor)), "backward"


def tendency_star(principal_star: int, monthly_star: int) -> tuple[int, bool]:
    natal_chart = fly_chart(principal_star)
    palace = next(key for key, value in natal_chart.items() if value == monthly_star)
    if palace == "C":
        return principal_star, True
    return HOME_STAR_BY_PALACE[palace], False


def _day_escapement(year: int, jd_tt: float, ephemeris: Ephemeris) -> tuple[bool, float]:
    try:
        summer = _summer_solstice(year, ephemeris)
        winter = _winter_solstice(year, ephemeris)
        previous_winter = _winter_solstice(year - 1, ephemeris)
    except ValueError:
        solar_lon = sun_longitude(jd_tt, ephemeris)
        if solar_lon >= 270.0 or solar_lon < 90.0:
            return True, _approx_winter_solstice(year if solar_lon >= 270.0 else year - 1)
        return False, _approx_summer_solstice(year)
    if jd_tt < summer:
        return True, previous_winter
    if jd_tt < winter:
        return False, summer
    return True, winter


def _summer_solstice(year: int, ephemeris: Ephemeris) -> float:
    return solar_term_crossing(
        90.0,
        jd_tt_from_utc(julian_day_utc(datetime(year, 6, 1, tzinfo=UTC))),
        jd_tt_from_utc(julian_day_utc(datetime(year, 7, 15, tzinfo=UTC))),
        ephemeris,
    )


def _winter_solstice(year: int, ephemeris: Ephemeris) -> float:
    return solar_term_crossing(
        270.0,
        jd_tt_from_utc(julian_day_utc(datetime(year, 12, 1, tzinfo=UTC))),
        jd_tt_from_utc(julian_day_utc(datetime(year + 1, 1, 15, tzinfo=UTC))),
        ephemeris,
    )


def _approx_summer_solstice(year: int) -> float:
    return float(julian_day_from_date(year, 6, 21))


def _approx_winter_solstice(year: int) -> float:
    return float(julian_day_from_date(year, 12, 22))


def _solstice_jdn(jd_tt: float) -> int:
    return int(jd_tt + 0.5)


def _jiazi_at_or_before(jdn: int) -> int:
    return jdn - ((jdn - DAY_JIAZI_JDN) % 60)


def _jiazi_after(jdn: int) -> int:
    return _jiazi_at_or_before(jdn) + 60


def _wrap_star(value: int) -> int:
    return ((value - 1) % 9) + 1
