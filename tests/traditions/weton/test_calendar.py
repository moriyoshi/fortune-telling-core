from datetime import datetime, timedelta, timezone

import pytest

from fortune_telling_core.traditions.weton.calendar import (
    PANCAWARA,
    SAPTAWARA,
    compute_weton,
)
from fortune_telling_core.traditions.weton.config import DayBoundary

_WIB = timezone(timedelta(hours=7))


def _at(year: int, month: int, day: int, hour: int = 12) -> datetime:
    return datetime(year, month, day, hour, tzinfo=_WIB)


@pytest.mark.parametrize(
    ("year", "month", "day", "expected", "neptu"),
    [
        (1945, 8, 17, "Jumat Legi", 11),  # Proclamation of Independence (anchor).
        (2000, 1, 1, "Sabtu Legi", 14),  # ki-demang almanac cross-check.
        (1990, 1, 1, "Senin Wage", 8),
    ],
)
def test_known_wetons(year: int, month: int, day: int, expected: str, neptu: int) -> None:
    chart = compute_weton(_at(year, month, day), DayBoundary.MIDNIGHT)

    assert chart.name == expected
    assert chart.neptu == neptu


def test_pancawara_cycles_every_five_days() -> None:
    base = _at(2024, 1, 1)
    for offset in range(20):
        moment = base + timedelta(days=offset)
        same = base + timedelta(days=offset + 5)
        assert (
            compute_weton(moment, DayBoundary.MIDNIGHT).pancawara
            is compute_weton(same, DayBoundary.MIDNIGHT).pancawara
        )


def test_sunset_boundary_advances_evening_births() -> None:
    midnight = compute_weton(_at(1945, 8, 17, hour=19), DayBoundary.MIDNIGHT)
    sunset = compute_weton(_at(1945, 8, 17, hour=19), DayBoundary.SUNSET)

    assert midnight.name == "Jumat Legi"
    assert sunset.name == "Sabtu Pahing"


def test_sunset_boundary_leaves_daytime_births_unchanged() -> None:
    assert (
        compute_weton(_at(1945, 8, 17, hour=10), DayBoundary.SUNSET).name
        == compute_weton(_at(1945, 8, 17, hour=10), DayBoundary.MIDNIGHT).name
    )


def test_cycle_data_is_well_formed() -> None:
    assert tuple(day.weekday for day in SAPTAWARA) == (0, 1, 2, 3, 4, 5, 6)
    assert tuple(pasaran.index for pasaran in PANCAWARA) == (0, 1, 2, 3, 4)
    assert {day.neptu for day in SAPTAWARA} == {3, 4, 5, 6, 7, 8, 9}
    assert {pasaran.neptu for pasaran in PANCAWARA} == {4, 5, 7, 8, 9}
