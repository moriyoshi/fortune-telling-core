import pytest

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.position import EclipticPosition


def test_ecliptic_position_latitude_is_optional_and_backward_compatible() -> None:
    legacy = EclipticPosition(721.0, -0.2)
    with_latitude = EclipticPosition(10.0, 0.1, -3.5)

    assert legacy.longitude == 1.0
    assert legacy.speed == -0.2
    assert legacy.latitude is None
    assert with_latitude.latitude == -3.5


def test_sun_matches_meeus_worked_example() -> None:
    """Meeus, Astronomical Algorithms, 2nd ed., ch. 25, 1992 Oct 13.0 TD."""

    ephemeris = BuiltinEphemeris()

    assert ephemeris.position(Body.SUN, 2448908.5).longitude == pytest.approx(199.90895, abs=0.01)
    assert ephemeris.position(Body.SUN, 2448908.5).latitude is None


def test_moon_matches_meeus_worked_example() -> None:
    """Meeus ch. 47, 1992 Apr 12.0 TD, apparent longitude and latitude."""

    ephemeris = BuiltinEphemeris()
    moon = ephemeris.position(Body.MOON, 2448724.5)

    assert moon.longitude == pytest.approx(133.167264, abs=0.05)
    assert moon.latitude == pytest.approx(-3.229126, abs=0.001)


def test_ecliptic_position_latitude_defaults_to_none() -> None:
    assert BuiltinEphemeris().position(Body.MERCURY, 2448976.5).latitude is None


@pytest.mark.parametrize(
    ("body", "longitude", "tolerance"),
    [
        (Body.MERCURY, 249.97022125493157, 0.05),
        (Body.VENUS, 313.081517698484, 0.05),
        (Body.MARS, 114.5596791556854, 0.05),
        (Body.JUPITER, 192.28564619037942, 0.1),
        (Body.SATURN, 315.1486613063138, 0.1),
        (Body.URANUS, 286.96958810764414, 0.1),
        (Body.NEPTUNE, 287.91148337529074, 0.1),
    ],
)
def test_vsop_planets_match_meeus_apparent_position_examples(
    body: Body, longitude: float, tolerance: float
) -> None:
    """Meeus ch. 33, 1992 Dec 20.0 TD RA/Dec examples converted to ecliptic longitude."""

    ephemeris = BuiltinEphemeris()

    assert ephemeris.position(body, 2448976.5).longitude == pytest.approx(longitude, abs=tolerance)


def test_pluto_matches_meeus_worked_example() -> None:
    """Meeus ch. 37, 1992 Oct 13.0 TD geocentric RA/Dec converted to ecliptic longitude."""

    ephemeris = BuiltinEphemeris()

    assert ephemeris.position(Body.PLUTO, 2448908.5).longitude == pytest.approx(
        231.69500917417508, abs=0.1
    )
