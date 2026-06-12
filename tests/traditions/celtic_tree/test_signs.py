from datetime import date, timedelta

import pytest

from fortune_telling_core.traditions.celtic_tree.signs import SIGNS, classify


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [
        (1, 1, "Birch"),  # wrap into January
        (1, 20, "Birch"),
        (1, 21, "Rowan"),  # boundary start
        (6, 9, "Hawthorn"),  # boundary end
        (6, 10, "Oak"),
        (2, 29, "Ash"),  # leap day
        (12, 22, "Elder"),
        (12, 23, "Elder"),  # Graves' nameless day, folded into Ruis
        (12, 24, "Birch"),
    ],
)
def test_classify_boundaries(month: int, day: int, expected: str) -> None:
    assert classify(date(2024, month, day)).tree == expected


def test_every_day_classifies_and_all_signs_used() -> None:
    seen = set()
    day = date(2024, 1, 1)  # a leap year
    while day.year == 2024:
        seen.add(classify(day).slug)
        day += timedelta(days=1)
    assert seen == {sign.slug for sign in SIGNS}


def test_ranges_are_contiguous() -> None:
    by_start = sorted(SIGNS, key=lambda s: (s.start_month, s.start_day))
    for current, following in zip(by_start, by_start[1:], strict=False):
        end_next = date(2024, current.end_month, current.end_day) + timedelta(days=1)
        assert (end_next.month, end_next.day) == (following.start_month, following.start_day)


def test_thirteen_signs() -> None:
    assert len(SIGNS) == 13
