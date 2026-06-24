"""Sun-sign (zodiac-sign-only) chart calculation.

A sun-sign reading needs only the querent's zodiac sign, not a full birth
chart: no birth time, latitude, or longitude. The sign is taken from an
explicit ``sun_sign`` attribute when supplied, otherwise classified from the
birth date using the conventional Western tropical date ranges in
:mod:`fortune_telling_core.traditions.astrology.dates`.

Because those date ranges are a tropical convention, sun-sign readings are
always tropical; sidereal sun signs are not well-defined from a date alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from fortune_telling_core._parsing import collect_values
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.astrology.bodies import Body
from fortune_telling_core.traditions.astrology.dates import (
    _coerce_sign,
    sign_for_date,
    zodiac_date_range,
)
from fortune_telling_core.traditions.astrology.spreads import SUN_SIGN
from fortune_telling_core.traditions.astrology.zodiac import TROPICAL_ZODIAC, Sign

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

_SYMBOLS_BY_ID = {symbol.id: symbol for symbol in TROPICAL_ZODIAC.symbols}


@dataclass(frozen=True, slots=True)
class SunSignInput:
    """The resolved sun sign and how it was determined.

    Attributes:
        sign: The zodiac sun sign.
        birth_date: The classified birth date, or ``None`` when the sign was
            supplied explicitly.
    """

    sign: Sign
    birth_date: date | None


def parse_sun_sign(request: ReadingRequest) -> SunSignInput:
    """Resolve the sun sign from a request.

    Accepts an explicit ``sun_sign`` (a :class:`Sign`, a sign symbol id, or a
    bare slug) in options or querent attributes. When absent, a ``birth_date``
    (or ``birth_datetime``) is required and classified into a sign using the
    conventional tropical date ranges; only the calendar date is consulted.

    Args:
        request: Reading request carrying ``sun_sign`` or ``birth_date`` in
            options or querent attributes.

    Returns:
        The resolved :class:`SunSignInput`.

    Raises:
        ValidationError: If neither input is present, or a value is malformed.
    """

    values = collect_values(request)
    explicit = values.get("sun_sign")
    if explicit:
        return SunSignInput(sign=_coerce_sign(explicit), birth_date=None)
    raw = values.get("birth_date") or values.get("birth_datetime")
    if not raw:
        raise ValidationError("sun_sign or birth_date is required")
    birth_date = _parse_date(raw)
    return SunSignInput(sign=_coerce_sign(sign_for_date(birth_date)), birth_date=birth_date)


def cast_sun_sign_draw(request: ReadingRequest) -> Draw:
    """Cast the sun-sign reading as a deterministic draw.

    Args:
        request: Reading request with ``sun_sign`` or ``birth_date``.

    Returns:
        A draw with a single ``sun`` selection on the tropical zodiac deck.

    Raises:
        ValidationError: If the sun-sign input is missing or malformed.
    """

    parsed = parse_sun_sign(request)
    sign = parsed.sign
    symbol = _SYMBOLS_BY_ID[sign.symbol_id]
    modifiers = {
        "sign": sign.display_name,
        "element": symbol.attributes["element"],
        "modality": symbol.attributes["modality"],
        "polarity": symbol.attributes["polarity"],
        "ruler": symbol.attributes["ruler"],
        "date_range": _format_range(zodiac_date_range(sign)),
        "source": "date" if parsed.birth_date is not None else "explicit",
    }
    if parsed.birth_date is not None:
        modifiers["birth_date"] = parsed.birth_date.isoformat()
    selection = Selection(
        position_id=Body.SUN.value,
        symbol_id=sign.symbol_id,
        modifiers=modifiers,
    )
    return Draw(TROPICAL_ZODIAC.id, SUN_SIGN.id, (selection,))


def _parse_date(raw: str) -> date:
    # ``datetime.fromisoformat`` accepts both a bare date ("1990-04-15") and a
    # full datetime; either way only the calendar date matters for the sign.
    try:
        return datetime.fromisoformat(raw).date()
    except ValueError:
        raise ValidationError("birth_date must be an ISO-8601 date") from None


def _format_range(bounds: tuple[tuple[int, int], tuple[int, int]]) -> str:
    (start_month, start_day), (end_month, end_day) = bounds
    start = f"{_MONTH_ABBR[start_month - 1]} {start_day}"
    end = f"{_MONTH_ABBR[end_month - 1]} {end_day}"
    return f"{start} – {end}"
