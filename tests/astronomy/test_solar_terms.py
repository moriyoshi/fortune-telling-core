import pytest

from fortune_telling_core.astronomy import (
    EclipticPosition,
    adjacent_jie_crossing,
    solar_month_index,
    solar_term_crossing,
)
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.traditions.four_pillars.solar_terms import (
    month_branch_index,
    months_since_yin,
)


class LinearSunEphemeris:
    id = "linear-sun"
    version = "1"

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        assert body == Body.SUN
        return EclipticPosition(jd_tt % 360.0, 1.0)

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset({Body.SUN})


def test_solar_month_index_starts_at_lichun() -> None:
    assert solar_month_index(315.0) == 0
    assert solar_month_index(344.999) == 0
    assert solar_month_index(345.0) == 1
    assert solar_month_index(314.999) == 11


def test_four_pillars_keeps_month_alias_and_branch_offset() -> None:
    assert months_since_yin(45.0) == solar_month_index(45.0)
    assert month_branch_index(315.0) == 2
    assert month_branch_index(45.0) == 5


def test_solar_term_crossing_wrapper_scans_until_target() -> None:
    assert solar_term_crossing(315.0, 300.0, 330.0, LinearSunEphemeris()) == pytest.approx(315.0)


def test_adjacent_jie_crossing_selects_previous_or_next_term() -> None:
    ephemeris = LinearSunEphemeris()

    assert adjacent_jie_crossing(320.0, ephemeris, forward=True) == pytest.approx(345.0)
    assert adjacent_jie_crossing(350.0, ephemeris, forward=False) == pytest.approx(345.0)
