from datetime import datetime, timedelta, timezone

import pytest

from fortune_telling_core.astronomy.julian import julian_day_from_date
from fortune_telling_core.traditions.can_chi.config import DayBoundary
from fortune_telling_core.traditions.can_chi.pillars import compute_chart
from fortune_telling_core.traditions.can_chi.stems_branches import can, chi
from fortune_telling_core.traditions.four_pillars.pillars import DAY_JIAZI_JDN
from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi

_ICT = timezone(timedelta(hours=7))


def _at(year: int, month: int, day: int, hour: int = 12) -> datetime:
    return datetime(year, month, day, hour, tzinfo=_ICT)


@pytest.mark.parametrize(
    ("year", "month", "day", "expected"),
    [
        (1984, 2, 2, "Giáp Tý"),  # shared anchor with Four Pillars.
        (2000, 1, 1, "Bính Thìn"),
        (1990, 4, 15, "Mậu Thân"),
    ],
)
def test_known_day_pillars(year: int, month: int, day: int, expected: str) -> None:
    chart = compute_chart(_at(year, month, day), DayBoundary.MIDNIGHT)
    name = f"{can(chart.day.can_index).name} {chi(chart.day.chi_index).name}"

    assert name == expected


def test_day_pillar_agrees_with_four_pillars_anchor() -> None:
    for offset in range(0, 400, 13):
        moment = _at(1984, 2, 2) + timedelta(days=offset)
        chart = compute_chart(moment, DayBoundary.MIDNIGHT)

        jdn = julian_day_from_date(moment.year, moment.month, moment.day)
        fp = ganzhi((jdn - DAY_JIAZI_JDN) % 60)
        assert chart.day.can_index == fp.stem_index
        assert chart.day.chi_index == fp.branch_index


def test_hour_branch_tracks_two_hour_periods() -> None:
    # 23:00-00:59 is the hour of Tý (branch 0); 11:00-12:59 is Ngọ (branch 6).
    assert compute_chart(_at(2000, 1, 1, hour=23), DayBoundary.MIDNIGHT).hour.chi_index == 0
    assert compute_chart(_at(2000, 1, 1, hour=0), DayBoundary.MIDNIGHT).hour.chi_index == 0
    assert compute_chart(_at(2000, 1, 1, hour=12), DayBoundary.MIDNIGHT).hour.chi_index == 6


def test_late_ty_boundary_advances_day_at_2300() -> None:
    midnight = compute_chart(_at(1984, 2, 2, hour=23), DayBoundary.MIDNIGHT)
    late_ty = compute_chart(_at(1984, 2, 2, hour=23), DayBoundary.LATE_TY)

    assert (midnight.day.can_index, midnight.day.chi_index) == (0, 0)  # Giáp Tý
    assert (late_ty.day.can_index, late_ty.day.chi_index) == (1, 1)  # Ất Sửu (next day)


def test_cat_and_buffalo_are_vietnamese_animals() -> None:
    assert chi(3).animal == "Cat"
    assert chi(1).animal == "Water Buffalo"
