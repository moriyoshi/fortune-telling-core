"""Sidereal ayanamsa helpers."""

from __future__ import annotations

from fortune_telling_core.traditions.astrology.config import Ayanamsa


def ayanamsa_degrees(jd_tt: float, ayanamsa: Ayanamsa) -> float:
    if ayanamsa != Ayanamsa.LAHIRI:
        raise ValueError(f"unsupported ayanamsa: {ayanamsa}")
    # Lahiri is about 23.85675 degrees at J2000, increasing by roughly 50.29 arcsec/year.
    years = (jd_tt - 2451545.0) / 365.2425
    return (23.85675 + years * (50.290966 / 3600.0)) % 360.0
