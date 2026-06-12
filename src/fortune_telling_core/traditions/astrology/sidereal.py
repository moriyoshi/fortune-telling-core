"""Sidereal conversion helpers."""

from __future__ import annotations

from fortune_telling_core.astronomy.position import normalize_degrees
from fortune_telling_core.traditions.astrology.ayanamsa import ayanamsa_degrees
from fortune_telling_core.traditions.astrology.config import Ayanamsa


def sidereal_longitude(tropical_longitude: float, jd_tt: float, ayanamsa: Ayanamsa) -> float:
    return normalize_degrees(tropical_longitude - ayanamsa_degrees(jd_tt, ayanamsa))
