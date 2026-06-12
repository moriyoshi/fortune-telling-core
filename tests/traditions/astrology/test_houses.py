import math

import pytest

from fortune_telling_core.traditions.astrology.config import HouseSystem
from fortune_telling_core.traditions.astrology.errors import PlacidusUndefinedError
from fortune_telling_core.traditions.astrology.houses import compute_houses, house_of

_REFERENCE_ASCENDANT = 204.28745089829405
_REFERENCE_MIDHEAVEN = 279.61104956646807
_REFERENCE_LATITUDE = 51.5
_REFERENCE_OBLIQUITY = 23.43782367964824
_REFERENCE_CUSPS = (
    204.287450898,
    61.161962135,
    82.030073953,
    99.611049566,
    119.053236371,
    147.687181909,
    24.287450898,
    241.161962135,
    262.030073953,
    279.611049566,
    299.053236371,
    327.687181909,
)


def test_whole_sign_and_equal_houses() -> None:
    whole = compute_houses(HouseSystem.WHOLE_SIGN, 17.0, 100.0, 35.0)
    equal = compute_houses(HouseSystem.EQUAL, 17.0, 100.0, 35.0)

    assert whole.cusps[0] == 0.0
    assert whole.cusps[1] == 30.0
    assert equal.cusps[0] == 17.0
    assert equal.cusps[1] == 47.0
    assert house_of(65.0, whole) == 3


def test_placidus_high_latitude_error_and_fallback() -> None:
    with pytest.raises(PlacidusUndefinedError):
        compute_houses(HouseSystem.PLACIDUS, 10.0, 100.0, 70.0)

    fallback = compute_houses(
        HouseSystem.PLACIDUS,
        10.0,
        100.0,
        70.0,
        high_latitude_fallback=True,
    )
    assert fallback.system == HouseSystem.WHOLE_SIGN.value


def test_placidus_semi_arc_reference_cusps() -> None:
    """Reference cusps from the published Placidus semi-arc geometry.

    Sources: Wikipedia, "House (astrology)", Placidus section
    (https://en.wikipedia.org/wiki/House_(astrology)#Placidus), for trisecting
    the IC-horizon and horizon-MC arcs; Jean Meeus, Astronomical Algorithms,
    2nd ed., chapter 13, for ecliptic longitude, right ascension, and declination
    transformations. The in-test bisection helper solves those equations
    independently of the production fixed-point iteration.
    """
    houses = compute_houses(
        HouseSystem.PLACIDUS,
        _REFERENCE_ASCENDANT,
        _REFERENCE_MIDHEAVEN,
        _REFERENCE_LATITUDE,
        obliquity=_REFERENCE_OBLIQUITY,
    )

    assert houses.cusps == pytest.approx(_REFERENCE_CUSPS, abs=1.0e-9)
    assert houses.cusps[1] == pytest.approx(_reference_placidus_cusp(60.0, 2.0 / 3.0))
    assert houses.cusps[2] == pytest.approx(_reference_placidus_cusp(120.0, 1.0 / 3.0))
    assert houses.cusps[10] == pytest.approx(_reference_placidus_cusp(0.0, 1.0 / 3.0))
    assert houses.cusps[11] == pytest.approx(_reference_placidus_cusp(0.0, 2.0 / 3.0))
    assert houses.cusps[0] == pytest.approx(_REFERENCE_ASCENDANT)
    assert houses.cusps[9] == pytest.approx(_REFERENCE_MIDHEAVEN)
    assert len(houses.cusps) == 12


def test_placidus_geometry_midheaven_keeps_shifted_zodiac_output() -> None:
    shifted = compute_houses(
        HouseSystem.PLACIDUS,
        _REFERENCE_ASCENDANT - 24.0,
        _REFERENCE_MIDHEAVEN - 24.0,
        _REFERENCE_LATITUDE,
        obliquity=_REFERENCE_OBLIQUITY,
        geometry_midheaven=_REFERENCE_MIDHEAVEN,
    )

    assert shifted.cusps == pytest.approx(
        tuple((cusp - 24.0) % 360.0 for cusp in _REFERENCE_CUSPS),
        abs=1.0e-9,
    )


def _reference_placidus_cusp(base_degrees: float, semi_arc_factor: float) -> float:
    ramc = _right_ascension(_REFERENCE_MIDHEAVEN)
    lower = 0.0
    upper = 180.0
    for _ in range(80):
        middle = (lower + upper) / 2.0
        value = _reference_equation(middle, ramc, base_degrees, semi_arc_factor)
        if value < 0.0:
            lower = middle
        else:
            upper = middle
    return _longitude_from_right_ascension(ramc + (lower + upper) / 2.0)


def _reference_equation(
    right_ascension_offset: float,
    ramc: float,
    base_degrees: float,
    semi_arc_factor: float,
) -> float:
    longitude = _longitude_from_right_ascension(ramc + right_ascension_offset)
    declination = _declination(longitude)
    semi_arc = math.degrees(
        math.acos(
            -math.tan(math.radians(_REFERENCE_LATITUDE)) * math.tan(math.radians(declination))
        )
    )
    return right_ascension_offset - base_degrees - semi_arc_factor * semi_arc


def _right_ascension(longitude: float) -> float:
    lon = math.radians(longitude)
    eps = math.radians(_REFERENCE_OBLIQUITY)
    return math.degrees(math.atan2(math.sin(lon) * math.cos(eps), math.cos(lon))) % 360.0


def _declination(longitude: float) -> float:
    lon = math.radians(longitude)
    eps = math.radians(_REFERENCE_OBLIQUITY)
    return math.degrees(math.asin(math.sin(eps) * math.sin(lon)))


def _longitude_from_right_ascension(right_ascension: float) -> float:
    ra = math.radians(right_ascension)
    eps = math.radians(_REFERENCE_OBLIQUITY)
    return math.degrees(math.atan2(math.sin(ra) / math.cos(eps), math.cos(ra))) % 360.0
