"""Hebrew gematria letter-value system.

Assigns each Hebrew letter its standard gematria value (mispar hechrachi):
units 1-9, tens 10-90, hundreds 100-400. The five final forms (sofit) either
share their base value (``standard``) or take the mispar gadol values 500-900
(``gadol``).

Niqqud (vowel points) and cantillation marks are stripped before evaluation and
recorded by the engine as ``vowels=ignored``. Whitespace and punctuation are
ignored. Any other unsupported character is rejected, per the No-Silent-Loss
policy for new value systems.
"""

from __future__ import annotations

from enum import StrEnum

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import (
    NameValueUnit,
    is_ignorable,
    strip_combining_marks,
)

ID = "hebrew_gematria.v1"
VERSION = "1"


class FinalLetterMode(StrEnum):
    """How the five Hebrew final forms (sofit) are valued.

    ``STANDARD`` gives each final form the same value as its base letter.
    ``GADOL`` (mispar gadol) gives the final forms the values 500-900.
    """

    STANDARD = "standard"
    GADOL = "gadol"


# Base 22 letters: mispar hechrachi values.
_BASE_VALUES = {
    "א": 1,
    "ב": 2,
    "ג": 3,
    "ד": 4,
    "ה": 5,
    "ו": 6,
    "ז": 7,
    "ח": 8,
    "ט": 9,
    "י": 10,
    "כ": 20,
    "ל": 30,
    "מ": 40,
    "נ": 50,
    "ס": 60,
    "ע": 70,
    "פ": 80,
    "צ": 90,
    "ק": 100,
    "ר": 200,
    "ש": 300,
    "ת": 400,
}

# Final forms (sofit) sharing their base letter's value.
_FINALS_STANDARD = {"ך": 20, "ם": 40, "ן": 50, "ף": 80, "ץ": 90}

# Final forms under mispar gadol.
_FINALS_GADOL = {"ך": 500, "ם": 600, "ן": 700, "ף": 800, "ץ": 900}

_TABLES = {
    FinalLetterMode.STANDARD: {**_BASE_VALUES, **_FINALS_STANDARD},
    FinalLetterMode.GADOL: {**_BASE_VALUES, **_FINALS_GADOL},
}


def values(
    name: str,
    *,
    final_letter_mode: FinalLetterMode = FinalLetterMode.STANDARD,
) -> tuple[NameValueUnit, ...]:
    """Return the per-letter gematria values for ``name``.

    Args:
        name: The Hebrew name or word to evaluate.
        final_letter_mode: Whether final forms take their base value
            (``STANDARD``) or the mispar gadol values (``GADOL``).

    Returns:
        One :class:`NameValueUnit` per Hebrew letter, in input order.

    Raises:
        ValidationError: If ``name`` contains a character that is neither a
            supported Hebrew letter nor ignorable whitespace or punctuation.
    """

    table = _TABLES[final_letter_mode]
    units: list[NameValueUnit] = []
    for char in strip_combining_marks(name):
        value = table.get(char)
        if value is not None:
            units.append(NameValueUnit(char, value))
        elif is_ignorable(char):
            continue
        else:
            raise ValidationError(
                f"unsupported character for Hebrew gematria: {char!r} (U+{ord(char):04X})"
            )
    return tuple(units)


def total(units: tuple[NameValueUnit, ...]) -> int:
    """Return the sum of the values in ``units``."""

    return sum(unit.value for unit in units)
