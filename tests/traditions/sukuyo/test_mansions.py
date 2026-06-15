import pytest

from fortune_telling_core.traditions.sukuyo.config import Ayanamsa
from fortune_telling_core.traditions.sukuyo.mansions import (
    MANSION_COUNT,
    MANSION_WIDTH,
    MANSIONS,
    ayanamsa_degrees,
    mansion_for_longitude,
)

_J2000 = 2451545.0


def test_mansions_partition_the_zodiac() -> None:
    assert MANSION_COUNT == 27
    assert pytest.approx(360.0) == MANSION_WIDTH * 27
    assert tuple(m.index for m in MANSIONS) == tuple(range(27))


def test_longitude_to_mansion_is_equal_13deg20_division() -> None:
    # With no ayanamsa, mansion 0 (Ashvini) starts at sidereal 0°, each spanning
    # 13°20′. These boundaries are the nakshatra division.
    cases = {
        0.0: ("ashvini", "婁宿"),
        13.4: ("bharani", "胃宿"),
        26.7: ("krittika", "昴宿"),
        180.0: ("chitra", "角宿"),
        359.9: ("revati", "奎宿"),
    }
    for longitude, (slug, cjk) in cases.items():
        mansion = mansion_for_longitude(longitude, _J2000, Ayanamsa.NONE)
        assert (mansion.slug, mansion.cjk) == (slug, cjk)


def test_lahiri_ayanamsa_matches_known_j2000_value() -> None:
    # Lahiri ayanamsa is ~23.85° at J2000; Fagan-Bradley ~24.74°; tropical 0.
    assert ayanamsa_degrees(_J2000, Ayanamsa.NONE) == 0.0
    assert ayanamsa_degrees(_J2000, Ayanamsa.LAHIRI) == pytest.approx(23.85, abs=0.05)
    assert ayanamsa_degrees(_J2000, Ayanamsa.FAGAN_BRADLEY) == pytest.approx(24.74, abs=0.05)


def test_ayanamsa_shifts_mansion_against_tropical() -> None:
    # A tropical longitude of 24° sits in Bharani; subtracting the ~23.85° Lahiri
    # ayanamsa pulls it back into Ashvini.
    assert mansion_for_longitude(24.0, _J2000, Ayanamsa.NONE).slug == "bharani"
    assert mansion_for_longitude(24.0, _J2000, Ayanamsa.LAHIRI).slug == "ashvini"
