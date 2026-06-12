from datetime import date, timedelta

import pytest

from fortune_telling_core.traditions.haab.months import MONTHS, YEAR_LENGTH, haab_for


@pytest.mark.parametrize(
    ("year", "month", "day", "expected"),
    [
        (2012, 12, 21, "3 K'ank'in"),  # GMT-correlation anchor (partner of 4 Ajaw).
        (2012, 12, 22, "4 K'ank'in"),
        (2013, 3, 28, "0 Wayeb'"),
        (2013, 4, 2, "0 Pop"),  # Haab' new year.
    ],
)
def test_known_haab_dates(year: int, month: int, day: int, expected: str) -> None:
    assert haab_for(date(year, month, day)).name == expected


def test_wayeb_has_five_days_then_rolls_to_pop() -> None:
    new_year = date(2013, 4, 2)  # 0 Pop
    last_wayeb = haab_for(new_year - timedelta(days=1))

    assert last_wayeb.month.slug == "wayeb"
    assert last_wayeb.day == 4  # Wayeb' runs 0..4


def test_year_repeats_every_365_days() -> None:
    base = date(2012, 12, 21)
    for offset in range(0, YEAR_LENGTH * 2, 29):
        assert (
            haab_for(base + timedelta(days=offset)).name
            == haab_for(base + timedelta(days=offset + YEAR_LENGTH)).name
        )


def test_month_lengths_sum_to_365() -> None:
    assert sum(month.length for month in MONTHS) == YEAR_LENGTH
    assert len(MONTHS) == 19
    assert MONTHS[18].length == 5
