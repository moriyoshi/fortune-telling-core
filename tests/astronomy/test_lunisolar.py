from datetime import datetime, timedelta, timezone

from fortune_telling_core.astronomy import BuiltinEphemeris, jd_tt_from_utc, julian_day_utc
from fortune_telling_core.astronomy.julian import julian_day_from_date
from fortune_telling_core.astronomy.lunisolar import (
    LunisolarDate,
    civil_day_number,
    to_lunisolar,
)

_JST = timezone(timedelta(hours=9))
_EPHEMERIS = BuiltinEphemeris()


def _convert(year: int, month: int, day: int) -> LunisolarDate:
    jd = jd_tt_from_utc(julian_day_utc(datetime(year, month, day, 12, 0, tzinfo=_JST)))
    return to_lunisolar(jd, tz_hours=9.0, ephemeris=_EPHEMERIS)


def test_civil_day_number_matches_julian_day_from_date() -> None:
    jd = jd_tt_from_utc(julian_day_utc(datetime(2024, 2, 10, 12, 0, tzinfo=_JST)))
    assert civil_day_number(jd, 9.0) == julian_day_from_date(2024, 2, 10)


def test_known_conversions() -> None:
    # Lunar New Year 2024 -> 1/1; Mid-Autumn 2024 -> 8/15.
    assert _convert(2024, 2, 10) == LunisolarDate(2024, 1, 1, False)
    assert _convert(2024, 9, 17) == LunisolarDate(2024, 8, 15, False)
    # Late-December Gregorian date still belongs to the prior lunar year.
    assert _convert(2024, 1, 1) == LunisolarDate(2023, 11, 20, False)


def test_leap_month_detection() -> None:
    # 2023 has a leap second month (閏二月): 1 Mar-22 is 閏2/1.
    assert _convert(2023, 3, 22) == LunisolarDate(2023, 2, 1, True)
    # The day before is the last day of the ordinary second month.
    assert _convert(2023, 3, 21) == LunisolarDate(2023, 2, 30, False)
    # The ordinary second month starts a lunation earlier and is not leap.
    assert _convert(2023, 2, 20) == LunisolarDate(2023, 2, 1, False)
    # 2014 has a leap ninth month (閏九月).
    assert _convert(2014, 10, 24) == LunisolarDate(2014, 9, 1, True)
