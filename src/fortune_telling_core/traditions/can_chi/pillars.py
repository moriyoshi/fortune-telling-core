"""Vietnamese Can Chi day and hour pillar computation.

Both pillars are pure calendar arithmetic — no ephemeris is required. The day
pillar shares Four Pillars' sexagenary anchor (2000-01-07 = Giáp Tý), so the
two traditions agree on every calendar day. The hour stem follows the same
five-rat (ngũ thử độn) rule used across the Sino-xenic systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from fortune_telling_core.astronomy.julian import julian_day_from_date
from fortune_telling_core.traditions.can_chi.config import DayBoundary

# 2000-01-07 is a Giáp Tý day, shared with Four Pillars' DAY_JIAZI_JDN.
_DAY_GIAPTY_JDN = julian_day_from_date(2000, 1, 7)


@dataclass(frozen=True, slots=True)
class Pillar:
    """A Can Chi pillar as separate stem and branch cycle indices."""

    can_index: int
    chi_index: int


@dataclass(frozen=True, slots=True)
class CanChiChart:
    day: Pillar
    hour: Pillar


def compute_chart(birth: datetime, day_boundary: DayBoundary) -> CanChiChart:
    """Compute the day and hour Can Chi pillars for a birth moment.

    Args:
        birth: Timezone-aware birth datetime, interpreted in its own offset.
        day_boundary: Whether the day pillar rolls over at midnight or at the
            late hour of Tý (23:00).

    Returns:
        The resolved day and hour pillars.
    """

    day_date = birth.date()
    if day_boundary is DayBoundary.LATE_TY and birth.hour == 23:
        day_date = (birth + timedelta(days=1)).date()
    day_jdn = julian_day_from_date(day_date.year, day_date.month, day_date.day)
    day_offset = (day_jdn - _DAY_GIAPTY_JDN) % 60
    day_can = day_offset % 10
    day_chi = day_offset % 12

    hour_chi = ((birth.hour + 1) // 2) % 12
    first_hour_can = (2 * (day_can % 5)) % 10
    hour_can = (first_hour_can + hour_chi) % 10

    return CanChiChart(Pillar(day_can, day_chi), Pillar(hour_can, hour_chi))
