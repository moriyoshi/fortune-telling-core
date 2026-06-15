from datetime import UTC, datetime

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.position import EclipticPosition
from fortune_telling_core.traditions.nine_star_ki.config import DayStarEscapement
from fortune_telling_core.traditions.nine_star_ki.lo_shu import LO_SHU_BASE, fly_chart
from fortune_telling_core.traditions.nine_star_ki.star_calc import (
    compute_chart,
    day_star,
    month_star,
    tendency_star,
    year_star,
    year_star_digit_root_oracle,
    year_star_digit_sum_oracle,
)
from fortune_telling_core.traditions.nine_star_ki.stars import HOME_PALACE, STARS


def test_star_data_integrity_and_lo_shu_magic_square() -> None:
    assert tuple(star.number for star in STARS) == tuple(range(1, 10))
    assert HOME_PALACE == {
        1: "N",
        2: "SW",
        3: "E",
        4: "SE",
        5: "C",
        6: "NW",
        7: "W",
        8: "NE",
        9: "S",
    }
    assert fly_chart(5) == LO_SHU_BASE

    rows = (("NW", "N", "NE"), ("W", "C", "E"), ("SW", "S", "SE"))
    cols = (("NW", "W", "SW"), ("N", "C", "S"), ("NE", "E", "SE"))
    diagonals = (("NW", "C", "SE"), ("NE", "C", "SW"))
    for line in rows + cols + diagonals:
        assert sum(LO_SHU_BASE[palace] for palace in line) == 15


def test_year_star_anchor_and_digit_sum_oracles() -> None:
    for solar_year, expected in ((1900, 1), (1901, 9), (1908, 2), (1984, 7), (2024, 3)):
        assert year_star(solar_year) == expected
        assert year_star_digit_sum_oracle(solar_year) == expected
        assert year_star_digit_root_oracle(solar_year) == expected


def test_month_star_table_by_year_star_group() -> None:
    assert [month_star(1, month) for month in range(4)] == [8, 7, 6, 5]
    assert [month_star(5, month) for month in range(4)] == [2, 1, 9, 8]
    assert [month_star(9, month) for month in range(4)] == [5, 4, 3, 2]


def test_day_star_direction_pinned_by_fixed_sun() -> None:
    winter_arc = _day(datetime(2024, 1, 10, tzinfo=UTC), 315.0)
    summer_arc = _day(datetime(2024, 7, 10, tzinfo=UTC), 180.0)

    assert winter_arc == (7, "forward")
    assert summer_arc == (1, "backward")


def test_day_star_escapement_school_can_shift_anchor() -> None:
    value = datetime(2024, 1, 10, tzinfo=UTC)
    ephemeris = _sun_at(315.0)
    jd_tt = jd_tt_from_utc(julian_day_utc(value))

    assert day_star(value, jd_tt, ephemeris, DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE) == (
        7,
        "forward",
    )
    assert day_star(value, jd_tt, ephemeris, DayStarEscapement.FIRST_JIAZI_AFTER_SOLSTICE) == (
        1,
        "forward",
    )


def test_tendency_star_and_center_case() -> None:
    assert tendency_star(1, 1) == (1, True)
    assert tendency_star(5, 5) == (5, True)
    assert tendency_star(1, 9) == (4, False)


def test_risshun_and_jie_boundaries_with_fixed_sun() -> None:
    before = compute_chart(
        datetime(2024, 2, 1, tzinfo=UTC),
        datetime(2024, 2, 1, tzinfo=UTC),
        _sun_at(314.0),
        2024,
    )
    after = compute_chart(
        datetime(2024, 2, 5, tzinfo=UTC),
        datetime(2024, 2, 5, tzinfo=UTC),
        _sun_at(315.0),
        2024,
    )
    next_month = compute_chart(
        datetime(2024, 3, 10, tzinfo=UTC),
        datetime(2024, 3, 10, tzinfo=UTC),
        _sun_at(345.0),
        2024,
    )

    assert before.solar_year == 2023
    assert after.solar_year == 2024
    assert after.solar_month_index == 0
    assert next_month.solar_month_index == 1


def _day(value: datetime, longitude: float) -> tuple[int, str]:
    ephemeris = _sun_at(longitude)
    return day_star(value, jd_tt_from_utc(julian_day_utc(value)), ephemeris)


def _sun_at(longitude: float) -> FixedEphemeris:
    return FixedEphemeris({Body.SUN: EclipticPosition(longitude, 1.0)})
