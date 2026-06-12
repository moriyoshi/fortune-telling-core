from datetime import date, timedelta

import pytest

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions.astrology.dates import (
    _DATE_RANGES,
    sign_for_date,
    zodiac_date_range,
)
from fortune_telling_core.traditions.astrology.zodiac import TROPICAL_ZODIAC, Sign


def test_accepts_slug_id_symbol_and_enum() -> None:
    expected = ((3, 21), (4, 19))
    assert zodiac_date_range("aries") == expected
    assert zodiac_date_range("astro.sign.aries") == expected
    assert zodiac_date_range(Sign.ARIES) == expected
    aries = next(s for s in TROPICAL_ZODIAC.symbols if s.id == "astro.sign.aries")
    assert zodiac_date_range(aries) == expected


def test_date_ranges_cover_every_sign() -> None:
    # Guard against the sign list drifting out of sync with the Sign enum.
    assert set(_DATE_RANGES) == set(Sign)


def test_wrapping_signs() -> None:
    assert zodiac_date_range("capricorn") == ((12, 22), (1, 19))
    assert zodiac_date_range("pisces") == ((2, 19), (3, 20))


def test_covers_every_deck_sign() -> None:
    for symbol in TROPICAL_ZODIAC.symbols:
        (start, end) = zodiac_date_range(symbol)
        assert 1 <= start[0] <= 12 and 1 <= start[1] <= 31
        assert 1 <= end[0] <= 12 and 1 <= end[1] <= 31


def test_unknown_sign_raises() -> None:
    with pytest.raises(ValidationError):
        zodiac_date_range("ophiuchus")


def test_sign_for_date_boundaries() -> None:
    assert sign_for_date(date(2021, 3, 21)) == "astro.sign.aries"
    assert sign_for_date(date(2021, 4, 19)) == "astro.sign.aries"
    assert sign_for_date(date(2021, 4, 20)) == "astro.sign.taurus"


def test_sign_for_date_wraps_new_year() -> None:
    assert sign_for_date(date(2021, 12, 22)) == "astro.sign.capricorn"
    assert sign_for_date(date(2021, 1, 1)) == "astro.sign.capricorn"
    assert sign_for_date(date(2021, 1, 19)) == "astro.sign.capricorn"


def test_sign_for_date_is_leap_year_correct() -> None:
    # 29 February falls inside Pisces and only exists in a leap year.
    assert sign_for_date(date(2020, 2, 29)) == "astro.sign.pisces"
    # The day after a leap day still lands in the same sign as a common year.
    assert sign_for_date(date(2020, 3, 1)) == sign_for_date(date(2021, 3, 1))


def test_sign_for_date_covers_every_day_of_year() -> None:
    # Use a leap year so 29 February is included; every day maps to exactly one
    # sign whose range round-trips back to contain the date.
    day = date(2020, 1, 1)
    while day.year == 2020:
        sign_id = sign_for_date(day)
        (start, end) = zodiac_date_range(sign_id)
        month_day = (day.month, day.day)
        if start <= end:
            assert start <= month_day <= end
        else:
            assert month_day >= start or month_day <= end
        day += timedelta(days=1)
