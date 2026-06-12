"""Pure-Python deterministic apparent geocentric ephemeris."""

from __future__ import annotations

import math

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.builtin_series import (
    MOON_LATITUDE_TERMS,
    MOON_LONGITUDE_DISTANCE_TERMS,
    PLUTO_ARGUMENTS,
    PLUTO_LATITUDE_TERMS,
    PLUTO_LONGITUDE_TERMS,
    PLUTO_RADIUS_TERMS,
    VSOP87D_SERIES,
)
from fortune_telling_core.astronomy.errors import EphemerisError
from fortune_telling_core.astronomy.julian import julian_centuries
from fortune_telling_core.astronomy.nutation import nutation_longitude
from fortune_telling_core.astronomy.position import EclipticPosition, normalize_degrees

_J2000 = 2451545.0
_LIGHT_TIME_DAYS_PER_AU = 0.0057755183
_ABERRATION_CONSTANT_ARCSEC = 20.4898
_PLANET_KEYS: dict[Body, str] = {
    Body.MERCURY: "mercury",
    Body.VENUS: "venus",
    Body.MARS: "mars",
    Body.JUPITER: "jupiter",
    Body.SATURN: "saturn",
    Body.URANUS: "uranus",
    Body.NEPTUNE: "neptune",
}


class BuiltinEphemeris:
    """Pure-Python deterministic ephemeris shipped with the package.

    The built-in backend keeps runtime dependencies empty and is suitable for
    deterministic tests and general symbolic work. It is not a replacement for
    a high-precision professional astronomy backend.

    Example:
        ```python
        from fortune_telling_core.astronomy import Body, BuiltinEphemeris

        ephemeris = BuiltinEphemeris()
        sun = ephemeris.position(Body.SUN, 2451545.0)
        ```
    """

    id = "astro.ephemeris.builtin"
    version = "0.2.1"

    def supported_bodies(self) -> frozenset[Body]:
        """Return all bodies accepted by the built-in ephemeris."""

        return frozenset(Body)

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        """Return an apparent geocentric ecliptic position.

        Args:
            body: Body to compute.
            jd_tt: Julian day on the Terrestrial Time scale.

        Returns:
            Ecliptic longitude, approximate longitude speed, and Moon latitude.

        Raises:
            EphemerisError: If ``body`` is not supported.
        """

        if body == Body.SOUTH_NODE:
            north = self.position(Body.NORTH_NODE, jd_tt)
            return EclipticPosition(north.longitude + 180.0, north.speed)
        longitude = _longitude(body, jd_tt)
        previous_lon = _longitude(body, jd_tt - 0.5)
        next_lon = _longitude(body, jd_tt + 0.5)
        speed = _signed_delta(next_lon, previous_lon)
        latitude = _latitude(body, jd_tt)
        return EclipticPosition(longitude, speed, latitude)


def _longitude(body: Body, jd_tt: float) -> float:
    if body == Body.SUN:
        return _sun_apparent_longitude(jd_tt)
    if body == Body.MOON:
        return _moon_apparent_longitude(jd_tt)
    if body == Body.NORTH_NODE:
        return _moon_true_node_longitude(jd_tt)
    if body == Body.PLUTO:
        return _planet_apparent_longitude("pluto", jd_tt)
    planet_key = _PLANET_KEYS.get(body)
    if planet_key is not None:
        return _planet_apparent_longitude(planet_key, jd_tt)
    raise EphemerisError(f"unsupported body: {body}")


def _latitude(body: Body, jd_tt: float) -> float | None:
    if body == Body.MOON:
        return _moon_ecliptic_latitude(jd_tt)
    return None


def _sun_apparent_longitude(jd_tt: float) -> float:
    t = julian_centuries(jd_tt)
    mean_longitude = normalize_degrees(280.46646 + 36000.76983 * t + 0.0003032 * t * t)
    mean_anomaly = math.radians(
        normalize_degrees(357.52911 + 35999.05029 * t - 0.0001537 * t * t + t**3 / 24490000.0)
    )
    center = (
        (1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(mean_anomaly)
        + (0.019993 - 0.000101 * t) * math.sin(2.0 * mean_anomaly)
        + 0.000289 * math.sin(3.0 * mean_anomaly)
    )
    radius = (
        1.000001018
        * (1.0 - (0.016708634 - 0.000042037 * t - 0.0000001267 * t * t) ** 2)
        / (
            1.0
            + (0.016708634 - 0.000042037 * t - 0.0000001267 * t * t)
            * math.cos(mean_anomaly + math.radians(center))
        )
    )
    aberration = -_ABERRATION_CONSTANT_ARCSEC / (3600.0 * radius)
    return normalize_degrees(mean_longitude + center + aberration + nutation_longitude(jd_tt))


def _planet_apparent_longitude(planet_key: str, jd_tt: float) -> float:
    earth = _heliocentric_rectangular("earth", jd_tt)
    planet = _heliocentric_rectangular(planet_key, jd_tt)
    geo = _vector_subtract(planet, earth)
    distance = _vector_length(geo)
    planet = _heliocentric_rectangular(planet_key, jd_tt - _LIGHT_TIME_DAYS_PER_AU * distance)
    geo = _vector_subtract(planet, earth)
    geometric = math.degrees(math.atan2(geo[1], geo[0]))
    latitude = math.atan2(geo[2], math.hypot(geo[0], geo[1]))
    aberration = _planet_aberration_longitude(jd_tt, math.radians(geometric), latitude)
    fk5 = _fk5_longitude_correction(jd_tt, math.radians(geometric), latitude)
    return normalize_degrees(geometric + aberration + fk5 + nutation_longitude(jd_tt))


def _planet_aberration_longitude(jd_tt: float, longitude: float, latitude: float) -> float:
    t = julian_centuries(jd_tt)
    eccentricity = 0.016708634 - 0.000042037 * t - 0.0000001267 * t * t
    perihelion = math.radians(102.93735 + 1.71946 * t + 0.00046 * t * t)
    earth_lon = _heliocentric_spherical("earth", jd_tt)[0]
    sun_lon = earth_lon + math.pi
    seconds = (
        _ABERRATION_CONSTANT_ARCSEC
        * (-math.cos(sun_lon - longitude) + eccentricity * math.cos(perihelion - longitude))
        / math.cos(latitude)
    )
    return seconds / 3600.0


def _fk5_longitude_correction(jd_tt: float, longitude: float, latitude: float) -> float:
    t = julian_centuries(jd_tt)
    longitude_prime = longitude - math.radians(t * (1.397 + 0.00031 * t))
    seconds = -0.09033 + 0.03916 * (
        math.cos(longitude_prime) + math.sin(longitude_prime)
    ) * math.tan(latitude)
    return seconds / 3600.0


def _heliocentric_rectangular(key: str, jd_tt: float) -> tuple[float, float, float]:
    lon, lat, radius = _heliocentric_spherical(key, jd_tt)
    cos_lat = math.cos(lat)
    return (
        radius * cos_lat * math.cos(lon),
        radius * cos_lat * math.sin(lon),
        radius * math.sin(lat),
    )


def _heliocentric_spherical(key: str, jd_tt: float) -> tuple[float, float, float]:
    if key == "pluto":
        return _pluto_heliocentric_spherical(jd_tt)
    series = VSOP87D_SERIES[key]
    tau = (jd_tt - _J2000) / 365250.0
    lon = _evaluate_vsop(series[0], tau)
    lat = _evaluate_vsop(series[1], tau)
    radius = _evaluate_vsop(series[2], tau)
    return lon % math.tau, lat, radius


def _evaluate_vsop(series: dict[int, tuple[tuple[float, float, float], ...]], tau: float) -> float:
    value = 0.0
    tau_power = 1.0
    for power in range(6):
        terms = series.get(power)
        if terms is not None:
            value += tau_power * sum(a * math.cos(b + c * tau) for a, b, c in terms)
        tau_power *= tau
    return value


def _pluto_heliocentric_spherical(jd_tt: float) -> tuple[float, float, float]:
    t = julian_centuries(jd_tt)
    jupiter = math.radians(34.35 + 3034.9057 * t)
    saturn = math.radians(50.08 + 1222.1138 * t)
    pluto = math.radians(238.96 + 144.96 * t)
    lon_correction = 0.0
    lat_correction = 0.0
    radius_correction = 0.0
    for index, multipliers in enumerate(PLUTO_ARGUMENTS):
        alpha = multipliers[0] * jupiter + multipliers[1] * saturn + multipliers[2] * pluto
        sin_alpha = math.sin(alpha)
        cos_alpha = math.cos(alpha)
        lon_correction += (
            PLUTO_LONGITUDE_TERMS[index][0] * sin_alpha
            + PLUTO_LONGITUDE_TERMS[index][1] * cos_alpha
        )
        lat_correction += (
            PLUTO_LATITUDE_TERMS[index][0] * sin_alpha + PLUTO_LATITUDE_TERMS[index][1] * cos_alpha
        )
        radius_correction += (
            PLUTO_RADIUS_TERMS[index][0] * sin_alpha + PLUTO_RADIUS_TERMS[index][1] * cos_alpha
        )
    lon = math.radians(238.958116 + 144.96 * t + lon_correction / 1_000_000.0)
    lat = math.radians(-3.908239 + lat_correction / 1_000_000.0)
    radius = 40.7241346 + radius_correction / 10_000_000.0
    return lon % math.tau, lat, radius


def _moon_apparent_longitude(jd_tt: float) -> float:
    t = julian_centuries(jd_tt)
    moon_mean_longitude, elongation, sun_anomaly, moon_anomaly, latitude_argument = _moon_arguments(
        t
    )
    eccentricity = 1.0 - 0.002516 * t - 0.0000074 * t * t
    arguments = (elongation, sun_anomaly, moon_anomaly, latitude_argument)
    longitude_sum = 0.0
    for (
        d_mult,
        m_mult,
        mp_mult,
        f_mult,
        longitude_coeff,
        _distance_coeff,
    ) in MOON_LONGITUDE_DISTANCE_TERMS:
        argument = (
            d_mult * arguments[0]
            + m_mult * arguments[1]
            + mp_mult * arguments[2]
            + f_mult * arguments[3]
        )
        longitude_sum += (
            longitude_coeff
            * _moon_eccentricity_factor(m_mult, eccentricity)
            * math.sin(math.radians(argument))
        )
    a1 = 119.75 + 131.849 * t
    a2 = 53.09 + 479264.290 * t
    longitude_sum += (
        3958.0 * math.sin(math.radians(a1))
        + 1962.0 * math.sin(math.radians(moon_mean_longitude - latitude_argument))
        + 318.0 * math.sin(math.radians(a2))
    )
    return normalize_degrees(
        moon_mean_longitude + longitude_sum / 1_000_000.0 + nutation_longitude(jd_tt)
    )


def _moon_ecliptic_latitude(jd_tt: float) -> float:
    t = julian_centuries(jd_tt)
    moon_mean_longitude, elongation, sun_anomaly, moon_anomaly, latitude_argument = _moon_arguments(
        t
    )
    eccentricity = 1.0 - 0.002516 * t - 0.0000074 * t * t
    arguments = (elongation, sun_anomaly, moon_anomaly, latitude_argument)
    latitude_sum = 0.0
    for d_mult, m_mult, mp_mult, f_mult, latitude_coeff in MOON_LATITUDE_TERMS:
        argument = (
            d_mult * arguments[0]
            + m_mult * arguments[1]
            + mp_mult * arguments[2]
            + f_mult * arguments[3]
        )
        latitude_sum += (
            latitude_coeff
            * _moon_eccentricity_factor(m_mult, eccentricity)
            * math.sin(math.radians(argument))
        )
    a1 = 119.75 + 131.849 * t
    a3 = 313.45 + 481266.484 * t
    latitude_sum += (
        -2235.0 * math.sin(math.radians(moon_mean_longitude))
        + 382.0 * math.sin(math.radians(a3))
        + 175.0 * math.sin(math.radians(a1 - latitude_argument))
        + 175.0 * math.sin(math.radians(a1 + latitude_argument))
        + 127.0 * math.sin(math.radians(moon_mean_longitude - moon_anomaly))
        - 115.0 * math.sin(math.radians(moon_mean_longitude + moon_anomaly))
    )
    return latitude_sum / 1_000_000.0


def _moon_true_node_longitude(jd_tt: float) -> float:
    t = julian_centuries(jd_tt)
    omega = _moon_fundamental_argument(
        125.0445479, -1934.1362891, 0.0020754, 1.0 / 467441.0, -1.0 / 60616000.0, t
    )
    _, elongation, sun_anomaly, moon_anomaly, latitude_argument = _moon_arguments(t)
    correction = (
        -1.4979 * math.sin(math.radians(2.0 * (elongation - latitude_argument)))
        - 0.1500 * math.sin(math.radians(sun_anomaly))
        - 0.1226 * math.sin(math.radians(2.0 * elongation))
        + 0.1176 * math.sin(math.radians(2.0 * latitude_argument))
        - 0.0801 * math.sin(math.radians(2.0 * (moon_anomaly - latitude_argument)))
    )
    return normalize_degrees(omega + correction)


def _moon_arguments(t: float) -> tuple[float, float, float, float, float]:
    moon_mean_longitude = normalize_degrees(
        218.3164477 + 481267.88123421 * t - 0.0015786 * t * t + t**3 / 538841.0 - t**4 / 65194000.0
    )
    elongation = _moon_fundamental_argument(
        297.8501921, 445267.1114034, -0.0018819, 1.0 / 545868.0, -1.0 / 113065000.0, t
    )
    sun_anomaly = _moon_fundamental_argument(
        357.5291092, 35999.0502909, -0.0001536, 1.0 / 24490000.0, 0.0, t
    )
    moon_anomaly = _moon_fundamental_argument(
        134.9633964, 477198.8675055, 0.0087414, 1.0 / 69699.0, -1.0 / 14712000.0, t
    )
    latitude_argument = _moon_fundamental_argument(
        93.2720950, 483202.0175233, -0.0036539, -1.0 / 3526000.0, 1.0 / 863310000.0, t
    )
    return moon_mean_longitude, elongation, sun_anomaly, moon_anomaly, latitude_argument


def _moon_fundamental_argument(
    constant: float,
    linear: float,
    quadratic: float,
    cubic: float,
    quartic: float,
    t: float,
) -> float:
    return normalize_degrees(
        constant + linear * t + quadratic * t * t + cubic * t**3 + quartic * t**4
    )


def _moon_eccentricity_factor(m_multiplier: float, eccentricity: float) -> float:
    if abs(m_multiplier) == 1.0:
        return eccentricity
    if abs(m_multiplier) == 2.0:
        return eccentricity * eccentricity
    return 1.0


def _vector_subtract(
    planet: tuple[float, float, float], earth: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (planet[0] - earth[0], planet[1] - earth[1], planet[2] - earth[2])


def _vector_length(vector: tuple[float, float, float]) -> float:
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])


def _signed_delta(next_lon: float, previous_lon: float) -> float:
    delta = normalize_degrees(next_lon - previous_lon)
    if delta > 180.0:
        delta -= 360.0
    return delta
