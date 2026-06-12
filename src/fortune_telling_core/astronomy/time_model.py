"""Shared effective civil-time models."""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import StrEnum

from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.solar import equation_of_time


class TimeModel(StrEnum):
    """Civil-time adjustment models used by date-based traditions.

    ``CLOCK`` keeps the supplied aware datetime unchanged. ``LOCAL_MEAN_TIME``
    shifts by longitude relative to the timezone offset. ``TRUE_SOLAR`` also
    applies the equation of time.
    """

    CLOCK = "clock"
    LOCAL_MEAN_TIME = "lmt"
    TRUE_SOLAR = "true_solar"


def effective_datetime(
    value: datetime, longitude: float, time_model: TimeModel, ephemeris: Ephemeris
) -> datetime:
    """Apply a tradition time model to an aware datetime.

    Args:
        value: Timezone-aware source datetime.
        longitude: Geographic longitude in degrees east.
        time_model: Time adjustment model to apply.
        ephemeris: Ephemeris backend used by true solar time.

    Returns:
        The adjusted datetime. The original timezone information is preserved.

    Raises:
        EphemerisError: If true solar time is requested and the backend cannot
            compute the Sun.
    """

    if time_model == TimeModel.CLOCK:
        return value
    offset = value.utcoffset()
    offset_hours = 0.0 if offset is None else offset.total_seconds() / 3600.0
    lmt_shift = longitude / 15.0 - offset_hours
    result = value + timedelta(hours=lmt_shift)
    if time_model == TimeModel.TRUE_SOLAR:
        jd_tt = jd_tt_from_utc(julian_day_utc(value))
        result += timedelta(minutes=equation_of_time(jd_tt, ephemeris))
    return result
