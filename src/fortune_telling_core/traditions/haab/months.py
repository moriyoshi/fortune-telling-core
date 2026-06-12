"""Maya Haab' month data and day computation.

The Haab' is the 365-day Mesoamerican "vague year": eighteen winal (months) of
twenty days each, followed by Wayeb', a short month of five unlucky days. A
Haab' date is a day position (0-19, or 0-4 in Wayeb') within a named month,
e.g. "3 K'ank'in". Positions use the 0-based epigraphic convention, where the
seating of a month is day 0.

The year is anchored to 21 December 2012 = 3 K'ank'in, the Haab' partner of the
Long Count 13.0.0.0.0 4 Ajaw under the GMT (584283) correlation. The Haab' and
Tzolk'in together name a day in the 18 980-day Calendar Round.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from fortune_telling_core.astronomy.julian import julian_day_from_date

WINAL_LENGTH = 20
WAYEB_LENGTH = 5
YEAR_LENGTH = 365


@dataclass(frozen=True, slots=True)
class Month:
    """A Haab' month (winal), or the five-day Wayeb'."""

    index: int
    slug: str
    name: str
    length: int

    @property
    def symbol_id(self) -> str:
        return f"haab.month.{self.slug}"


MONTHS: tuple[Month, ...] = (
    Month(0, "pop", "Pop", WINAL_LENGTH),
    Month(1, "wo", "Wo'", WINAL_LENGTH),
    Month(2, "sip", "Sip", WINAL_LENGTH),
    Month(3, "sotz", "Sotz'", WINAL_LENGTH),
    Month(4, "sek", "Sek", WINAL_LENGTH),
    Month(5, "xul", "Xul", WINAL_LENGTH),
    Month(6, "yaxkin", "Yaxk'in", WINAL_LENGTH),
    Month(7, "mol", "Mol", WINAL_LENGTH),
    Month(8, "chen", "Ch'en", WINAL_LENGTH),
    Month(9, "yax", "Yax", WINAL_LENGTH),
    Month(10, "sak", "Sak", WINAL_LENGTH),
    Month(11, "keh", "Keh", WINAL_LENGTH),
    Month(12, "mak", "Mak", WINAL_LENGTH),
    Month(13, "kankin", "K'ank'in", WINAL_LENGTH),
    Month(14, "muwan", "Muwan", WINAL_LENGTH),
    Month(15, "pax", "Pax", WINAL_LENGTH),
    Month(16, "kayab", "K'ayab", WINAL_LENGTH),
    Month(17, "kumku", "Kumk'u", WINAL_LENGTH),
    Month(18, "wayeb", "Wayeb'", WAYEB_LENGTH),
)

MONTH_BY_SLUG = {month.slug: month for month in MONTHS}

# 21 December 2012 is 3 K'ank'in: month index 13, day 3 -> year position 263.
_ANCHOR_JDN = julian_day_from_date(2012, 12, 21)
_ANCHOR_POSITION = 13 * WINAL_LENGTH + 3


@dataclass(frozen=True, slots=True)
class HaabDate:
    """A Haab' date: a day position within a named month."""

    month: Month
    day: int

    @property
    def name(self) -> str:
        """Combined Haab' name, e.g. ``"3 K'ank'in"``."""

        return f"{self.day} {self.month.name}"


def haab_for(day: date) -> HaabDate:
    """Return the Haab' date for a calendar date.

    Args:
        day: Gregorian calendar date.

    Returns:
        The month and day position within the 365-day Haab' year.
    """

    delta = julian_day_from_date(day.year, day.month, day.day) - _ANCHOR_JDN
    position = (_ANCHOR_POSITION + delta) % YEAR_LENGTH
    return HaabDate(MONTHS[position // WINAL_LENGTH], position % WINAL_LENGTH)
