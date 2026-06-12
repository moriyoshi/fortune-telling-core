"""Conventional sun-sign date ranges."""

from __future__ import annotations

from datetime import date

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.symbols import Symbol
from fortune_telling_core.traditions.astrology.zodiac import Sign

MonthDay = tuple[int, int]
"""A calendar boundary as ``(month, day)``, independent of any year."""

# Common Western tropical sun-sign date ranges, keyed by sign. The bounds are
# inclusive ``(month, day)`` pairs. Exact crossings drift by roughly a day from
# year to year (and across published tables); these are the conventional
# boundaries rather than astronomically computed ones for a specific year.
# Capricorn and Pisces wrap across the year boundary (start month > end month).
_DATE_RANGES: dict[Sign, tuple[MonthDay, MonthDay]] = {
    Sign.ARIES: ((3, 21), (4, 19)),
    Sign.TAURUS: ((4, 20), (5, 20)),
    Sign.GEMINI: ((5, 21), (6, 20)),
    Sign.CANCER: ((6, 21), (7, 22)),
    Sign.LEO: ((7, 23), (8, 22)),
    Sign.VIRGO: ((8, 23), (9, 22)),
    Sign.LIBRA: ((9, 23), (10, 22)),
    Sign.SCORPIO: ((10, 23), (11, 21)),
    Sign.SAGITTARIUS: ((11, 22), (12, 21)),
    Sign.CAPRICORN: ((12, 22), (1, 19)),
    Sign.AQUARIUS: ((1, 20), (2, 18)),
    Sign.PISCES: ((2, 19), (3, 20)),
}


def _coerce_sign(sign: str | Sign | Symbol) -> Sign:
    raw = sign.id if isinstance(sign, Symbol) else str(sign)
    try:
        return Sign(raw.removeprefix("astro.sign."))
    except ValueError:
        raise ValidationError(f"unknown zodiac sign: {sign!r}") from None


def zodiac_date_range(sign: str | Sign | Symbol) -> tuple[MonthDay, MonthDay]:
    """Return the conventional sun-sign date range for a zodiac sign.

    The range uses the common Western tropical convention and is expressed as
    year-independent ``(month, day)`` boundaries, both inclusive. Capricorn and
    Pisces wrap across the new year, so their start boundary falls in a later
    month than their end boundary.

    Args:
        sign: A zodiac sign as a :class:`Sign`, a Symbol, a symbol id (e.g.
            ``"astro.sign.aries"``) or a bare slug (e.g. ``"aries"``).

    Returns:
        A ``(start, end)`` tuple of inclusive ``(month, day)`` boundaries.

    Raises:
        ValidationError: If the sign is not a recognised zodiac sign.
    """
    return _DATE_RANGES[_coerce_sign(sign)]


def sign_for_date(value: date) -> str:
    """Return the sign symbol id whose conventional range contains a date.

    Classification compares on ``(month, day)`` against the same Western
    tropical boundaries as :func:`zodiac_date_range`, so it is correct in both
    common and leap years (including 29 February). Only the month and day of
    ``value`` are consulted; the year is otherwise ignored.

    These are conventional boundaries, not an astronomically exact ingress: for
    a precise sun sign on a given instant, cast a reading with the astrology
    engine instead.

    Args:
        value: The calendar date to classify.

    Returns:
        The matching sign symbol id, e.g. ``"astro.sign.aries"``.
    """
    month_day = (value.month, value.day)
    for sign, (start, end) in _DATE_RANGES.items():
        if start <= end:
            within = start <= month_day <= end
        else:  # range wraps across the new year (Capricorn, Pisces)
            within = month_day >= start or month_day <= end
        if within:
            return sign.symbol_id
    raise ValidationError(f"no zodiac sign for date: {value!r}")  # pragma: no cover
