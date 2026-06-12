"""Ascendant and Midheaven calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass

from fortune_telling_core.astronomy.nutation import nutation_longitude, true_obliquity
from fortune_telling_core.astronomy.position import normalize_degrees
from fortune_telling_core.traditions.astrology.bodies import Angle


@dataclass(frozen=True, slots=True)
class ChartAngles:
    ascendant: float
    midheaven: float

    def by_id(self, angle: Angle) -> float:
        if angle == Angle.ASCENDANT:
            return self.ascendant
        return self.midheaven


def _gast(jd_ut: float, jd_tt: float) -> float:
    t = (jd_ut - 2451545.0) / 36525.0
    gmst = (
        280.46061837
        + 360.98564736629 * (jd_ut - 2451545.0)
        + 0.000387933 * t * t
        - t * t * t / 38710000.0
    )
    return normalize_degrees(
        gmst + nutation_longitude(jd_tt) * math.cos(math.radians(true_obliquity(jd_tt)))
    )


def local_sidereal_time(jd_ut: float, jd_tt: float, longitude: float) -> float:
    return normalize_degrees(_gast(jd_ut, jd_tt) + longitude)


def compute_angles(jd_ut: float, jd_tt: float, latitude: float, longitude: float) -> ChartAngles:
    lst = math.radians(local_sidereal_time(jd_ut, jd_tt, longitude))
    eps = math.radians(true_obliquity(jd_tt))
    lat = math.radians(latitude)

    mc = normalize_degrees(math.degrees(math.atan2(math.sin(lst), math.cos(lst) * math.cos(eps))))
    asc = normalize_degrees(
        math.degrees(
            math.atan2(
                -math.cos(lst),
                math.sin(lst) * math.cos(eps) + math.tan(lat) * math.sin(eps),
            )
        )
    )
    return ChartAngles(ascendant=asc, midheaven=mc)
