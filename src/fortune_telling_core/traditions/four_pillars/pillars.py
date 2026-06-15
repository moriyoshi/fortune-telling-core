"""Four Pillars computation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_from_date, julian_day_utc
from fortune_telling_core.astronomy.solar import sun_longitude
from fortune_telling_core.traditions.four_pillars.config import DayBoundary, LuckDirectionInput
from fortune_telling_core.traditions.four_pillars.luck import luck_forward
from fortune_telling_core.traditions.four_pillars.sexagenary import annual_index, ganzhi, index_for
from fortune_telling_core.traditions.four_pillars.solar_terms import (
    adjacent_jie_crossing,
    month_branch_index,
)

# 2000-01-07 is a Jia-Zi (甲子) day, the day-pillar sexagenary anchor.
# Note: this engine's previous anchor, 1984-02-02, is NOT Jia-Zi — 万年暦
# lookups place it at Bing-Yin / 丙寅, two days later in the cycle. 1984 is a
# Jia-Zi *year*, which likely prompted the earlier (mistaken) day anchor.
DAY_JIAZI_JDN = julian_day_from_date(2000, 1, 7)


@dataclass(frozen=True, slots=True)
class PillarSet:
    year_index: int
    month_index: int
    day_index: int
    hour_index: int
    luck_forward: bool
    luck_start_age: float


def compute_pillars(
    birth_datetime: datetime,
    effective_dt: datetime,
    ephemeris: Ephemeris,
    gender: LuckDirectionInput,
    day_boundary: DayBoundary,
) -> PillarSet:
    jd_ut = julian_day_utc(birth_datetime)
    jd_tt = jd_tt_from_utc(jd_ut)
    solar_lon = sun_longitude(jd_tt, ephemeris)
    local_year = effective_dt.year
    year_for_pillar = local_year
    try:
        if jd_tt < _lichun_for_year(local_year, ephemeris):
            year_for_pillar -= 1
    except ValueError:
        if solar_lon < 315.0 and effective_dt.month <= 2:
            year_for_pillar -= 1
    year_index = annual_index(year_for_pillar)
    year_stem = ganzhi(year_index).stem_index

    month_branch = month_branch_index(solar_lon)
    months_from_yin = (month_branch - 2) % 12
    first_month_stem = (2 + 2 * (year_stem % 5)) % 10
    month_stem = (first_month_stem + months_from_yin) % 10
    month_index = index_for(month_stem, month_branch)

    day_date = effective_dt.date()
    if day_boundary == DayBoundary.LATE_ZISHI and effective_dt.hour == 23:
        day_date = (effective_dt + timedelta(days=1)).date()
    day_jdn = julian_day_from_date(day_date.year, day_date.month, day_date.day)
    day_index = (day_jdn - DAY_JIAZI_JDN) % 60
    day_stem = ganzhi(day_index).stem_index

    hour_branch = ((effective_dt.hour + 1) // 2) % 12
    first_hour_stem = (2 * (day_stem % 5)) % 10
    hour_stem = (first_hour_stem + hour_branch) % 10
    hour_index = index_for(hour_stem, hour_branch)

    forward = luck_forward(year_stem, gender)
    start_age = _luck_start_age(jd_tt, ephemeris, forward)
    return PillarSet(year_index, month_index, day_index, hour_index, forward, start_age)


def _lichun_for_year(year: int, ephemeris: Ephemeris) -> float:
    from fortune_telling_core.traditions.four_pillars.solar_terms import lichun_crossing

    return lichun_crossing(year, ephemeris)


def _luck_start_age(jd_tt: float, ephemeris: Ephemeris, forward: bool) -> float:
    try:
        crossing = adjacent_jie_crossing(jd_tt, ephemeris, forward=forward)
    except ValueError:
        crossing = jd_tt + (30.0 if forward else -30.0)
    return abs(crossing - jd_tt) / 3.0
