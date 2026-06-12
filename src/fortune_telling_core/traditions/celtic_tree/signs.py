"""Celtic tree calendar sign data and date classification.

This is the modern "Celtic tree zodiac" derived from Robert Graves' *The White
Goddess* (1948), which mapped thirteen Ogham letters to thirteen ~28-day lunar
months and their trees. It is a 20th-century reconstruction, not an attested
ancient Celtic calendar, but it is the form popularised as Celtic tree
astrology.

Graves leaves 23 December as a "nameless day" outside the thirteen months. To
keep classification total — every date maps to exactly one sign — that day is
folded into the preceding sign, Ruis (Elder), so its range runs 25 Nov – 23 Dec.

Ranges are fixed ``(month, day)`` boundaries compared as tuples, so the mapping
is leap-year correct by construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

_MONTH_ABBR = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


@dataclass(frozen=True, slots=True)
class TreeSign:
    """A Celtic tree sign: an Ogham letter, its tree, and its date range."""

    index: int
    slug: str
    ogham: str
    tree: str
    start_month: int
    start_day: int
    end_month: int
    end_day: int

    @property
    def symbol_id(self) -> str:
        return f"celtic_tree.sign.{self.slug}"

    @property
    def date_range(self) -> str:
        """Human-readable range, e.g. ``"Dec 24 – Jan 20"``."""

        start = f"{_MONTH_ABBR[self.start_month - 1]} {self.start_day}"
        end = f"{_MONTH_ABBR[self.end_month - 1]} {self.end_day}"
        return f"{start} – {end}"


SIGNS: tuple[TreeSign, ...] = (
    TreeSign(0, "birch", "Beth", "Birch", 12, 24, 1, 20),
    TreeSign(1, "rowan", "Luis", "Rowan", 1, 21, 2, 17),
    TreeSign(2, "ash", "Nion", "Ash", 2, 18, 3, 17),
    TreeSign(3, "alder", "Fearn", "Alder", 3, 18, 4, 14),
    TreeSign(4, "willow", "Saille", "Willow", 4, 15, 5, 12),
    TreeSign(5, "hawthorn", "Uath", "Hawthorn", 5, 13, 6, 9),
    TreeSign(6, "oak", "Duir", "Oak", 6, 10, 7, 7),
    TreeSign(7, "holly", "Tinne", "Holly", 7, 8, 8, 4),
    TreeSign(8, "hazel", "Coll", "Hazel", 8, 5, 9, 1),
    TreeSign(9, "vine", "Muin", "Vine", 9, 2, 9, 29),
    TreeSign(10, "ivy", "Gort", "Ivy", 9, 30, 10, 27),
    TreeSign(11, "reed", "Ngetal", "Reed", 10, 28, 11, 24),
    TreeSign(12, "elder", "Ruis", "Elder", 11, 25, 12, 23),
)

SIGN_BY_SLUG = {sign.slug: sign for sign in SIGNS}

# Signs ordered by start boundary; Beth (Dec 24) is the greatest and also the
# wrap-around sign for dates earlier than the first start of the year.
_BY_START = sorted(SIGNS, key=lambda sign: (sign.start_month, sign.start_day))


def classify(day: date) -> TreeSign:
    """Return the Celtic tree sign for a calendar date.

    Args:
        day: Gregorian calendar date.

    Returns:
        The tree sign whose range contains the date.
    """

    target = (day.month, day.day)
    chosen = _BY_START[-1]  # Beth, covering the late-December wrap into January.
    for sign in _BY_START:
        if (sign.start_month, sign.start_day) <= target:
            chosen = sign
    return chosen
