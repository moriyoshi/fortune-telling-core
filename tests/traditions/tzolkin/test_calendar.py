from datetime import date, timedelta

import pytest

from fortune_telling_core.traditions.tzolkin.daysigns import (
    DAYSIGNS,
    ROUND_LENGTH,
    tzolkin_for,
)


@pytest.mark.parametrize(
    ("year", "month", "day", "expected"),
    [
        (2012, 12, 21, "4 Ajaw"),  # GMT-correlation anchor.
        (2000, 1, 1, "11 Ik'"),
        (1987, 8, 17, "2 Ik'"),
    ],
)
def test_known_tzolkin_days(year: int, month: int, day: int, expected: str) -> None:
    assert tzolkin_for(date(year, month, day)).name == expected


def test_round_repeats_every_260_days() -> None:
    base = date(2012, 12, 21)
    for offset in range(0, ROUND_LENGTH * 2, 17):
        today = tzolkin_for(base + timedelta(days=offset))
        later = tzolkin_for(base + timedelta(days=offset + ROUND_LENGTH))
        assert today.name == later.name


def test_number_and_sign_advance_independently() -> None:
    base = date(2012, 12, 21)
    first = tzolkin_for(base)
    second = tzolkin_for(base + timedelta(days=1))

    assert second.number == first.number % 13 + 1
    assert second.sign.index == (first.sign.index + 1) % 20


def test_directions_cycle_east_north_west_south() -> None:
    assert tuple(sign.direction for sign in DAYSIGNS[:4]) == ("east", "north", "west", "south")
    assert DAYSIGNS[4].direction == "east"
