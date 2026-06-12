"""House cusp calculations."""

from __future__ import annotations

import math

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions.astrology.config import HouseSystem
from fortune_telling_core.traditions.astrology.errors import PlacidusUndefinedError
from fortune_telling_core.traditions.astrology.positions import Houses, normalize_degrees
from fortune_telling_core.traditions.astrology.zodiac import Sign

_J2000_MEAN_OBLIQUITY = 23.43929111111111
_PLACIDUS_TOLERANCE = 1.0e-12
_PLACIDUS_MAX_ITERATIONS = 50


def sign_index(longitude: float) -> int:
    return int(normalize_degrees(longitude) // 30.0)


def sign_id(longitude: float) -> str:
    return tuple(Sign)[sign_index(longitude)].symbol_id


def degree_in_sign(longitude: float) -> float:
    return normalize_degrees(longitude) % 30.0


def whole_sign_houses(ascendant: float) -> Houses:
    first = sign_index(ascendant) * 30.0
    return Houses(
        HouseSystem.WHOLE_SIGN.value,
        tuple(normalize_degrees(first + index * 30.0) for index in range(12)),
    )


def equal_houses(ascendant: float) -> Houses:
    return Houses(
        HouseSystem.EQUAL.value,
        tuple(normalize_degrees(ascendant + index * 30.0) for index in range(12)),
    )


def placidus_houses(
    ascendant: float,
    midheaven: float,
    latitude: float,
    *,
    obliquity: float = _J2000_MEAN_OBLIQUITY,
    geometry_midheaven: float | None = None,
) -> Houses:
    if abs(latitude) >= 66.0:
        raise PlacidusUndefinedError("Placidus houses are undefined at this high latitude")
    cusp_1 = normalize_degrees(ascendant)
    cusp_10 = normalize_degrees(midheaven)
    cusp_4 = normalize_degrees(cusp_10 + 180.0)
    cusp_7 = normalize_degrees(cusp_1 + 180.0)
    geometry_mc = cusp_10 if geometry_midheaven is None else normalize_degrees(geometry_midheaven)
    coordinate_offset = normalize_degrees(cusp_10 - geometry_mc)
    ramc = _ecliptic_right_ascension(geometry_mc, obliquity)
    cusps = [0.0] * 12
    cusps[0] = cusp_1
    cusps[3] = cusp_4
    cusps[6] = cusp_7
    cusps[9] = cusp_10
    cusp_11 = _solve_placidus_cusp(ramc, latitude, obliquity, 0.0, 1.0 / 3.0, 30.0)
    cusp_12 = _solve_placidus_cusp(ramc, latitude, obliquity, 0.0, 2.0 / 3.0, 60.0)
    cusp_2 = _solve_placidus_cusp(ramc, latitude, obliquity, 60.0, 2.0 / 3.0, 120.0)
    cusp_3 = _solve_placidus_cusp(ramc, latitude, obliquity, 120.0, 1.0 / 3.0, 150.0)
    cusps[10] = normalize_degrees(cusp_11 + coordinate_offset)
    cusps[11] = normalize_degrees(cusp_12 + coordinate_offset)
    cusps[1] = normalize_degrees(cusp_2 + coordinate_offset)
    cusps[2] = normalize_degrees(cusp_3 + coordinate_offset)
    cusps[4] = normalize_degrees(cusps[10] + 180.0)
    cusps[5] = normalize_degrees(cusps[11] + 180.0)
    cusps[7] = normalize_degrees(cusps[1] + 180.0)
    cusps[8] = normalize_degrees(cusps[2] + 180.0)
    return Houses(HouseSystem.PLACIDUS.value, tuple(cusps))


def compute_houses(
    system: HouseSystem,
    ascendant: float,
    midheaven: float,
    latitude: float,
    *,
    high_latitude_fallback: bool = False,
    obliquity: float = _J2000_MEAN_OBLIQUITY,
    geometry_midheaven: float | None = None,
) -> Houses:
    if system == HouseSystem.WHOLE_SIGN:
        return whole_sign_houses(ascendant)
    if system == HouseSystem.EQUAL:
        return equal_houses(ascendant)
    if system == HouseSystem.PLACIDUS:
        try:
            return placidus_houses(
                ascendant,
                midheaven,
                latitude,
                obliquity=obliquity,
                geometry_midheaven=geometry_midheaven,
            )
        except PlacidusUndefinedError:
            if high_latitude_fallback:
                return whole_sign_houses(ascendant)
            raise
    raise ValidationError(f"unsupported house system: {system}")


def house_of(longitude: float, houses: Houses) -> int:
    target = normalize_degrees(longitude)
    cusps = tuple(houses.cusps)
    for index, cusp in enumerate(cusps):
        next_cusp = cusps[(index + 1) % 12]
        arc = normalize_degrees(next_cusp - cusp)
        offset = normalize_degrees(target - cusp)
        if offset < arc or math.isclose(offset, arc):
            return index + 1
    return 12


def _solve_placidus_cusp(
    ramc: float,
    latitude: float,
    obliquity: float,
    base_degrees: float,
    semi_arc_factor: float,
    initial_ra_offset: float,
) -> float:
    longitude = _ecliptic_longitude_from_right_ascension(ramc + initial_ra_offset, obliquity)
    for _ in range(_PLACIDUS_MAX_ITERATIONS):
        declination = _ecliptic_declination(longitude, obliquity)
        semi_arc = _diurnal_semi_arc(latitude, declination)
        next_longitude = _ecliptic_longitude_from_right_ascension(
            ramc + base_degrees + semi_arc_factor * semi_arc,
            obliquity,
        )
        if abs(_signed_degrees(next_longitude - longitude)) <= _PLACIDUS_TOLERANCE:
            return next_longitude
        longitude = next_longitude
    raise PlacidusUndefinedError("Placidus cusp iteration did not converge")


def _diurnal_semi_arc(latitude: float, declination: float) -> float:
    lat = math.radians(latitude)
    dec = math.radians(declination)
    cosine_hour_angle = -math.tan(lat) * math.tan(dec)
    if cosine_hour_angle < -1.0 or cosine_hour_angle > 1.0:
        raise PlacidusUndefinedError("Placidus houses are undefined at this latitude")
    return math.degrees(math.acos(cosine_hour_angle))


def _ecliptic_declination(longitude: float, obliquity: float) -> float:
    lon = math.radians(longitude)
    eps = math.radians(obliquity)
    return math.degrees(math.asin(math.sin(eps) * math.sin(lon)))


def _ecliptic_right_ascension(longitude: float, obliquity: float) -> float:
    lon = math.radians(longitude)
    eps = math.radians(obliquity)
    return normalize_degrees(math.degrees(math.atan2(math.sin(lon) * math.cos(eps), math.cos(lon))))


def _ecliptic_longitude_from_right_ascension(
    right_ascension: float,
    obliquity: float,
) -> float:
    ra = math.radians(right_ascension)
    eps = math.radians(obliquity)
    return normalize_degrees(math.degrees(math.atan2(math.sin(ra) / math.cos(eps), math.cos(ra))))


def _signed_degrees(angle: float) -> float:
    return (angle + 180.0) % 360.0 - 180.0
