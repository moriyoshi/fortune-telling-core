from datetime import datetime, timedelta, timezone

import pytest

from fortune_telling_core.traditions.thaksa.chart import compute_chart
from fortune_telling_core.traditions.thaksa.houses import HOUSES

_ICT = timezone(timedelta(hours=7))


def _at(year: int, month: int, day: int, hour: int = 9) -> datetime:
    return datetime(year, month, day, hour, tzinfo=_ICT)


def test_sunday_birth_seats_sun_in_boriwan() -> None:
    chart = compute_chart(_at(1990, 4, 15))  # a Sunday

    placements = dict(
        zip((h.slug for h in HOUSES), (g.name for g in chart.placements), strict=True)
    )
    assert chart.ruler.name == "Sun"
    assert placements == {
        "boriwan": "Sun",
        "ayu": "Moon",
        "det": "Mars",
        "si": "Mercury",
        "mula": "Saturn",
        "utsaha": "Jupiter",
        "montri": "Rahu",
        "kalakini": "Venus",
    }
    assert chart.kalakini.name == "Venus"


def test_wednesday_day_rules_under_mercury() -> None:
    chart = compute_chart(_at(2000, 1, 5, hour=10))  # a Wednesday, daytime

    assert chart.ruler.name == "Mercury"
    assert chart.night is False
    assert chart.kalakini.name == "Mars"


def test_wednesday_night_rules_under_rahu() -> None:
    chart = compute_chart(_at(2000, 1, 5, hour=18))  # a Wednesday, 18:00

    assert chart.ruler.name == "Rahu"
    assert chart.night is True
    assert chart.kalakini.name == "Jupiter"


def test_every_birthday_uses_all_eight_grahas_once() -> None:
    # Mon..Sun in early Jan 2024 (2024-01-01 is a Monday); plus Wed night.
    moments = [_at(2024, 1, 1 + offset) for offset in range(7)]
    moments.append(_at(2024, 1, 3, hour=20))  # Wednesday night -> Rahu
    for moment in moments:
        names = {graha.name for graha in compute_chart(moment).placements}
        assert len(names) == 8


@pytest.mark.parametrize("hour", [0, 6, 12, 17])
def test_wednesday_before_evening_stays_mercury(hour: int) -> None:
    assert compute_chart(_at(2000, 1, 5, hour=hour)).ruler.name == "Mercury"
