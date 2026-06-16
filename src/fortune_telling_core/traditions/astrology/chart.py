"""Natal chart calculation."""

from __future__ import annotations

from datetime import datetime

from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.nutation import true_obliquity
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.astrology.angles import compute_angles
from fortune_telling_core.traditions.astrology.aspects import aspect_extras
from fortune_telling_core.traditions.astrology.birth import BirthData
from fortune_telling_core.traditions.astrology.bodies import PLANETARY_BODIES, Angle, Body
from fortune_telling_core.traditions.astrology.config import ZodiacMode
from fortune_telling_core.traditions.astrology.houses import (
    compute_houses,
    degree_in_sign,
    house_of,
    sign_id,
)
from fortune_telling_core.traditions.astrology.sidereal import sidereal_longitude
from fortune_telling_core.traditions.astrology.spreads import NATAL_CHART
from fortune_telling_core.traditions.astrology.zodiac import SIDEREAL_ZODIAC, TROPICAL_ZODIAC


def cast_draw(
    birth: BirthData, ephemeris: Ephemeris, *, transit_at: datetime | None = None
) -> Draw:
    jd_ut = julian_day_utc(birth.birth_datetime)
    jd_tt = jd_tt_from_utc(jd_ut)
    angles = compute_angles(jd_ut, jd_tt, birth.latitude, birth.longitude)

    transit_jd_tt = None if transit_at is None else jd_tt_from_utc(julian_day_utc(transit_at))

    ascendant = _zodiac_longitude(angles.ascendant, birth, jd_tt)
    midheaven = _zodiac_longitude(angles.midheaven, birth, jd_tt)
    houses = compute_houses(
        birth.config.house_system,
        ascendant,
        midheaven,
        birth.latitude,
        high_latitude_fallback=birth.config.high_latitude_fallback,
        obliquity=true_obliquity(jd_tt),
        geometry_midheaven=angles.midheaven,
    )

    selections: list[Selection] = []
    natal_longitudes: dict[str, float] = {}
    transit_longitudes: dict[str, float] = {}
    for body in PLANETARY_BODIES:
        position = ephemeris.position(body, jd_tt)
        longitude = _zodiac_longitude(position.longitude, birth, jd_tt)
        natal_longitudes[body.value] = longitude
        extra: dict[str, str] | None = None
        if transit_jd_tt is not None and transit_at is not None:
            transit = ephemeris.position(body, transit_jd_tt)
            transit_longitude = _zodiac_longitude(transit.longitude, birth, transit_jd_tt)
            extra = {
                "transit_longitude": f"{transit_longitude:.6f}",
                "transit_speed": f"{transit.speed:.6f}",
                "transit_retrograde": "true" if transit.speed < 0.0 else "false",
            }
            if body is PLANETARY_BODIES[0]:
                extra["transit_at"] = transit_at.isoformat()
            # The mirror node duplicates its opposite's aspects; keep it out of
            # the transiting set (mirrors the summary's exclusion).
            if body is not Body.SOUTH_NODE:
                transit_longitudes[body.value] = transit_longitude
        selections.append(
            _selection(
                body.value, longitude, position.speed, house_of(longitude, houses), extra=extra
            )
        )

    selections.append(
        _selection(Angle.ASCENDANT.value, ascendant, 0.0, house_of(ascendant, houses))
    )
    selections.append(
        _selection(Angle.MIDHEAVEN.value, midheaven, 0.0, house_of(midheaven, houses))
    )
    if birth.config.include_angles_in_aspects:
        natal_longitudes[Angle.ASCENDANT.value] = ascendant
        natal_longitudes[Angle.MIDHEAVEN.value] = midheaven

    extras = aspect_extras(
        natal_longitudes, transit_longitudes if transit_jd_tt is not None else None
    )

    deck_id = (
        SIDEREAL_ZODIAC.id if birth.config.zodiac == ZodiacMode.SIDEREAL else TROPICAL_ZODIAC.id
    )
    return Draw(
        deck_id=deck_id, spread_id=NATAL_CHART.id, selections=tuple(selections), extras=extras
    )


def _zodiac_longitude(longitude: float, birth: BirthData, jd_tt: float) -> float:
    if birth.config.zodiac == ZodiacMode.SIDEREAL:
        if birth.config.ayanamsa is None:
            raise AssertionError("sidereal config requires ayanamsa")
        return sidereal_longitude(longitude, jd_tt, birth.config.ayanamsa)
    return longitude


def _selection(
    position_id: str,
    longitude: float,
    speed: float,
    house: int,
    *,
    extra: dict[str, str] | None = None,
) -> Selection:
    modifiers = {
        "degree": f"{degree_in_sign(longitude):.6f}",
        "house": str(house),
        "longitude": f"{longitude:.6f}",
        "retrograde": "true" if speed < 0.0 else "false",
        "speed": f"{speed:.6f}",
    }
    if extra is not None:
        modifiers.update(extra)
    return Selection(position_id=position_id, symbol_id=sign_id(longitude), modifiers=modifiers)
