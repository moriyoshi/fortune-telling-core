from datetime import UTC, datetime

import pytest

from fortune_telling_core.astronomy import BuiltinEphemeris, EclipticPosition, julian_day_utc
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import delta_t_seconds
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.solar import equation_of_time, solar_longitude_crossing


class LinearSunEphemeris:
    id = "linear-sun"
    version = "1"

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        assert body == Body.SUN
        return EclipticPosition(jd_tt % 360.0, 1.0)

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset({Body.SUN})


def test_julian_day_j2000() -> None:
    assert julian_day_utc(datetime(2000, 1, 1, 12, tzinfo=UTC)) == 2451545.0


def test_delta_t_continuity() -> None:
    assert abs(delta_t_seconds(1999.9) - delta_t_seconds(2000.1)) < 5.0


def test_solar_longitude_crossing_wrap_and_unbracketed() -> None:
    crossing = solar_longitude_crossing(0.0, 359.0, 361.0, LinearSunEphemeris())
    assert crossing == pytest.approx(360.0, abs=1e-5)

    with pytest.raises(ValueError):
        solar_longitude_crossing(30.0, 100.0, 101.0, LinearSunEphemeris())


def test_equation_of_time_reasonable_range() -> None:
    assert abs(equation_of_time(2451545.0, BuiltinEphemeris())) <= 16.0


def test_fixed_ephemeris_sun_can_pin_terms() -> None:
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(315.0, 1.0)})
    assert ephemeris.position(Body.SUN, 0.0).longitude == 315.0
