"""Maya Tzolk'in day-sign data and day computation.

The Tzolk'in is the 260-day Mesoamerican sacred round: twenty named day signs
turning against thirteen trecena numbers, so a day is named by a number (1-13)
and a sign (e.g. "4 Ajaw"). Both cycles advance by one each day, returning to
the same pairing every 260 days.

Day signs are given in their Yucatec Maya names with the conventional English
keyword and the cardinal direction each sign carries (East, North, West, South,
repeating). The cycle is anchored to 21 December 2012 = 4 Ajaw under the
Goodman-Martínez-Thompson correlation (GMT, correlation constant 584283).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from fortune_telling_core.astronomy.julian import julian_day_from_date

_DIRECTIONS = ("east", "north", "west", "south")


@dataclass(frozen=True, slots=True)
class DaySign:
    """One of the twenty Tzolk'in day signs."""

    index: int
    slug: str
    name: str
    keyword: str

    @property
    def direction(self) -> str:
        """Cardinal direction carried by the sign."""

        return _DIRECTIONS[self.index % 4]

    @property
    def symbol_id(self) -> str:
        return f"tzolkin.daysign.{self.slug}"


DAYSIGNS: tuple[DaySign, ...] = (
    DaySign(0, "imix", "Imix", "Waterlily"),
    DaySign(1, "ik", "Ik'", "Wind"),
    DaySign(2, "akbal", "Ak'b'al", "Night"),
    DaySign(3, "kan", "K'an", "Seed"),
    DaySign(4, "chikchan", "Chikchan", "Serpent"),
    DaySign(5, "kimi", "Kimi", "Death"),
    DaySign(6, "manik", "Manik'", "Deer"),
    DaySign(7, "lamat", "Lamat", "Rabbit"),
    DaySign(8, "muluk", "Muluk", "Water"),
    DaySign(9, "ok", "Ok", "Dog"),
    DaySign(10, "chuwen", "Chuwen", "Monkey"),
    DaySign(11, "eb", "Eb", "Road"),
    DaySign(12, "ben", "B'en", "Reed"),
    DaySign(13, "ix", "Ix", "Jaguar"),
    DaySign(14, "men", "Men", "Eagle"),
    DaySign(15, "kib", "Kib'", "Owl"),
    DaySign(16, "kaban", "Kab'an", "Earth"),
    DaySign(17, "etznab", "Etz'nab'", "Flint"),
    DaySign(18, "kawak", "Kawak", "Storm"),
    DaySign(19, "ajaw", "Ajaw", "Lord"),
)

DAYSIGN_BY_SLUG = {sign.slug: sign for sign in DAYSIGNS}

# 21 December 2012 is 4 Ajaw under the GMT (584283) correlation.
_ANCHOR_JDN = julian_day_from_date(2012, 12, 21)
_ANCHOR_NUMBER = 4
_ANCHOR_SIGN = 19  # Ajaw

TRECENA_LENGTH = 13
ROUND_LENGTH = 260


@dataclass(frozen=True, slots=True)
class TzolkinDay:
    """A Tzolk'in day: a trecena number paired with a day sign."""

    number: int
    sign: DaySign

    @property
    def name(self) -> str:
        """Combined day name, e.g. ``"4 Ajaw"``."""

        return f"{self.number} {self.sign.name}"


def tzolkin_for(day: date) -> TzolkinDay:
    """Return the Tzolk'in day for a calendar date.

    Args:
        day: Gregorian calendar date.

    Returns:
        The trecena number and day sign for the date.
    """

    delta = julian_day_from_date(day.year, day.month, day.day) - _ANCHOR_JDN
    number = (delta + _ANCHOR_NUMBER - 1) % TRECENA_LENGTH + 1
    sign = DAYSIGNS[(delta + _ANCHOR_SIGN) % 20]
    return TzolkinDay(number, sign)
