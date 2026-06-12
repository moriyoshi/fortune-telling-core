"""Javanese saptawara/pancawara calendar data and weton computation.

The weton is the pairing of the seven-day week (*saptawara*) with the five-day
market week (*pancawara*, also called *pasaran*). Each cycle member carries a
*neptu* value; their sum is the weton neptu used throughout Javanese *primbon*
divination.

The pancawara phase is anchored to 17 August 1945, the Indonesian Proclamation
of Independence, which is historically recorded as *Jumat Legi* (neptu 11).
The saptawara is read directly from the proleptic Gregorian weekday, so the
anchor only fixes the five-day market cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from fortune_telling_core.traditions.weton.config import DayBoundary


@dataclass(frozen=True, slots=True)
class Saptawara:
    """A day of the seven-day Javanese week."""

    weekday: int
    """Proleptic Gregorian weekday, Monday=0 through Sunday=6."""

    slug: str
    name: str
    javanese: str
    neptu: int

    @property
    def symbol_id(self) -> str:
        return f"weton.saptawara.{self.slug}"


@dataclass(frozen=True, slots=True)
class Pancawara:
    """A day of the five-day Javanese market week (pasaran)."""

    index: int
    """Cycle position, 0=Legi through 4=Kliwon, relative to the anchor."""

    slug: str
    name: str
    javanese: str
    neptu: int

    @property
    def symbol_id(self) -> str:
        return f"weton.pancawara.{self.slug}"


# Ordered by proleptic Gregorian weekday (Monday=0 .. Sunday=6).
SAPTAWARA: tuple[Saptawara, ...] = (
    Saptawara(0, "senin", "Senin", "Senèn", 4),
    Saptawara(1, "selasa", "Selasa", "Selasa", 3),
    Saptawara(2, "rabu", "Rabu", "Rebo", 7),
    Saptawara(3, "kamis", "Kamis", "Kemis", 8),
    Saptawara(4, "jumat", "Jumat", "Jemuwah", 6),
    Saptawara(5, "sabtu", "Sabtu", "Setu", 9),
    Saptawara(6, "minggu", "Minggu", "Ngahad", 5),
)

# Ordered by pancawara cycle position (Legi=0 .. Kliwon=4).
PANCAWARA: tuple[Pancawara, ...] = (
    Pancawara(0, "legi", "Legi", "Legi", 5),
    Pancawara(1, "pahing", "Pahing", "Paing", 9),
    Pancawara(2, "pon", "Pon", "Pon", 7),
    Pancawara(3, "wage", "Wage", "Wagé", 4),
    Pancawara(4, "kliwon", "Kliwon", "Kliwon", 8),
)

SAPTAWARA_BY_SLUG = {day.slug: day for day in SAPTAWARA}
PANCAWARA_BY_SLUG = {pasaran.slug: pasaran for pasaran in PANCAWARA}

# 17 August 1945 (Jumat Legi) anchors the pancawara cycle to Legi.
_PASARAN_ANCHOR = date(1945, 8, 17).toordinal()

# Local-clock hour at which the SUNSET day boundary advances to the next weton.
_SUNSET_HOUR = 18


@dataclass(frozen=True, slots=True)
class WetonChart:
    """A resolved weton: a saptawara paired with a pancawara."""

    saptawara: Saptawara
    pancawara: Pancawara

    @property
    def neptu(self) -> int:
        """Combined neptu of the day and the pasaran."""

        return self.saptawara.neptu + self.pancawara.neptu

    @property
    def name(self) -> str:
        """Indonesian weton name, e.g. ``"Jumat Legi"``."""

        return f"{self.saptawara.name} {self.pancawara.name}"


def saptawara_for(day: date) -> Saptawara:
    """Return the saptawara for a calendar date."""

    return SAPTAWARA[day.weekday()]


def pancawara_for(day: date) -> Pancawara:
    """Return the pancawara (pasaran) for a calendar date."""

    return PANCAWARA[(day.toordinal() - _PASARAN_ANCHOR) % 5]


def compute_weton(birth: datetime, day_boundary: DayBoundary) -> WetonChart:
    """Compute the weton for a birth moment.

    Args:
        birth: Timezone-aware birth datetime. Its wall-clock date and hour are
            interpreted in the supplied offset.
        day_boundary: Whether the Javanese day rolls over at midnight or at the
            18:00 sunset approximation.

    Returns:
        The resolved weton chart.
    """

    day = birth.date()
    if day_boundary is DayBoundary.SUNSET and birth.hour >= _SUNSET_HOUR:
        day = date.fromordinal(day.toordinal() + 1)
    return WetonChart(saptawara_for(day), pancawara_for(day))
