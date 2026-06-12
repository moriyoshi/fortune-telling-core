import pytest

from fortune_telling_core.traditions.astrology.bodies import Body
from fortune_telling_core.traditions.astrology.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.traditions.astrology.positions import EclipticPosition


def test_builtin_ephemeris_reference_vectors() -> None:
    ephemeris = BuiltinEphemeris()
    jd_j2000 = 2451545.0

    assert ephemeris.position(Body.SUN, jd_j2000).longitude == pytest.approx(280.3724726857837)
    assert ephemeris.position(Body.MOON, jd_j2000).longitude == pytest.approx(223.31481342819714)
    assert ephemeris.position(Body.MERCURY, jd_j2000).longitude == pytest.approx(271.8881057102977)
    assert ephemeris.position(Body.NORTH_NODE, jd_j2000).speed < 0.0


def test_fixed_ephemeris_derives_south_node() -> None:
    from fortune_telling_core.traditions.astrology.ephemeris.fixed import FixedEphemeris

    ephemeris = FixedEphemeris({Body.NORTH_NODE: EclipticPosition(10.0, -0.1)})

    assert ephemeris.position(Body.SOUTH_NODE, 0.0).longitude == 190.0
