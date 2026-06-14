from datetime import UTC, datetime, timedelta

import pytest

from fortune_telling_core.astronomy import EclipticPosition, TimeModel, effective_datetime
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.solar import equation_of_time
from fortune_telling_core.traditions.four_pillars.config import TimeModel as FourPillarsTimeModel
from fortune_telling_core.traditions.four_pillars.time_model import (
    effective_datetime as four_pillars_effective_datetime,
)


def test_time_model_clock_returns_input_datetime() -> None:
    value = datetime(2024, 1, 1, 12, tzinfo=UTC)
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(0.0, 1.0)})

    assert effective_datetime(value, 135.0, TimeModel.CLOCK, ephemeris) == value


def test_time_model_local_mean_time_uses_longitude_offset() -> None:
    value = datetime(2024, 1, 1, 12, tzinfo=UTC)
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(0.0, 1.0)})

    assert effective_datetime(
        value, 30.0, TimeModel.LOCAL_MEAN_TIME, ephemeris
    ) == value + timedelta(hours=2)


def test_time_model_true_solar_adds_equation_of_time() -> None:
    value = datetime(2024, 1, 1, 12, tzinfo=UTC)
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(315.0, 1.0)})
    jd_tt = jd_tt_from_utc(julian_day_utc(value))
    expected_minutes = equation_of_time(jd_tt, ephemeris)

    result = effective_datetime(value, 0.0, TimeModel.TRUE_SOLAR, ephemeris)

    assert result == pytest.approx(
        value + timedelta(minutes=expected_minutes), abs=timedelta(seconds=1)
    )


def test_four_pillars_reexports_shared_time_model() -> None:
    assert FourPillarsTimeModel is TimeModel
    assert four_pillars_effective_datetime is effective_datetime
