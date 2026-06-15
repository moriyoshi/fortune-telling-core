"""Sukuyō 27-mansion table and sidereal helpers.

The Japanese Sukuyō system uses 27 lunar mansions (二十七宿) — the 28 Chinese
mansions with 牛宿 removed — which coincide with the 27 nakshatras. The mansions
are listed here in nakshatra order so that mansion ``0`` begins at sidereal
ecliptic longitude 0° (Aśvinī). A birth mansion is the equal 13°20′ division of
the Moon's sidereal longitude that the Moon occupies.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.sukuyo.config import Ayanamsa

MANSION_COUNT = 27
MANSION_WIDTH = 360.0 / MANSION_COUNT  # 13°20′

# Lahiri ayanamsa at J2000.0, in degrees, and the precession rate per year.
_LAHIRI_J2000 = 23.853
_FAGAN_BRADLEY_J2000 = 24.736
_PRECESSION_DEG_PER_YEAR = 0.0139644  # ~50.27″/yr
_J2000_JD = 2451545.0
_DAYS_PER_YEAR = 365.25


@dataclass(frozen=True, slots=True)
class Mansion:
    """A Sukuyō lunar mansion."""

    index: int
    slug: str
    cjk: str
    nakshatra: str


# Mansion 0 starts at sidereal 0° (Aśvinī); slugs use the unique nakshatra
# transliteration, with the Japanese 宿 carried in ``cjk``.
MANSIONS: tuple[Mansion, ...] = (
    Mansion(0, "ashvini", "婁宿", "Ashvini"),
    Mansion(1, "bharani", "胃宿", "Bharani"),
    Mansion(2, "krittika", "昴宿", "Krittika"),
    Mansion(3, "rohini", "畢宿", "Rohini"),
    Mansion(4, "mrigashira", "觜宿", "Mrigashira"),
    Mansion(5, "ardra", "参宿", "Ardra"),
    Mansion(6, "punarvasu", "井宿", "Punarvasu"),
    Mansion(7, "pushya", "鬼宿", "Pushya"),
    Mansion(8, "ashlesha", "柳宿", "Ashlesha"),
    Mansion(9, "magha", "星宿", "Magha"),
    Mansion(10, "purva_phalguni", "張宿", "Purva Phalguni"),
    Mansion(11, "uttara_phalguni", "翼宿", "Uttara Phalguni"),
    Mansion(12, "hasta", "軫宿", "Hasta"),
    Mansion(13, "chitra", "角宿", "Chitra"),
    Mansion(14, "svati", "亢宿", "Svati"),
    Mansion(15, "vishakha", "氐宿", "Vishakha"),
    Mansion(16, "anuradha", "房宿", "Anuradha"),
    Mansion(17, "jyeshtha", "心宿", "Jyeshtha"),
    Mansion(18, "mula", "尾宿", "Mula"),
    Mansion(19, "purva_ashadha", "箕宿", "Purva Ashadha"),
    Mansion(20, "uttara_ashadha", "斗宿", "Uttara Ashadha"),
    Mansion(21, "shravana", "女宿", "Shravana"),
    Mansion(22, "dhanishtha", "虚宿", "Dhanishtha"),
    Mansion(23, "shatabhisha", "危宿", "Shatabhisha"),
    Mansion(24, "purva_bhadrapada", "室宿", "Purva Bhadrapada"),
    Mansion(25, "uttara_bhadrapada", "壁宿", "Uttara Bhadrapada"),
    Mansion(26, "revati", "奎宿", "Revati"),
)


def ayanamsa_degrees(jd_tt: float, ayanamsa: Ayanamsa) -> float:
    """Return the ayanamsa in degrees for a Terrestrial-Time Julian day."""

    if ayanamsa == Ayanamsa.NONE:
        return 0.0
    base = _LAHIRI_J2000 if ayanamsa == Ayanamsa.LAHIRI else _FAGAN_BRADLEY_J2000
    years = (jd_tt - _J2000_JD) / _DAYS_PER_YEAR
    return base + years * _PRECESSION_DEG_PER_YEAR


def mansion_for_longitude(tropical_longitude: float, jd_tt: float, ayanamsa: Ayanamsa) -> Mansion:
    """Return the mansion occupied by a tropical Moon longitude."""

    sidereal = (tropical_longitude - ayanamsa_degrees(jd_tt, ayanamsa)) % 360.0
    return MANSIONS[int(sidereal / MANSION_WIDTH) % MANSION_COUNT]
