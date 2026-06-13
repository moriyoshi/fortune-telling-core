"""Latin Pythagorean letter-value system.

Assigns each ASCII letter A-Z a value from its alphabet position modulo nine
(A=1 … I=9, J=1 …, R=9, S=1 … Z=8). This is the reusable value table behind the
``name_numerology`` tradition engine.

For backward compatibility with the historical name-numerology contract, case
is folded and any character outside A-Z is ignored. The No-Silent-Loss policy
in the design note applies to new value systems; the Latin tables remain a
documented compatibility exception until a major release.
"""

from __future__ import annotations

import unicodedata
from enum import StrEnum
from string import ascii_uppercase

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import NameValueUnit, is_ignorable

ID = "latin_pythagorean.v1"
VERSION = "1"

LETTER_VALUES = {letter: index % 9 + 1 for index, letter in enumerate(ascii_uppercase)}


class NormalizationMode(StrEnum):
    """Latin Pythagorean normalization modes."""

    LATIN_ASCII_IGNORE = "latin_ascii_ignore"
    LATIN_ACCENT_FOLD = "latin_accent_fold"


def values(
    name: str,
    *,
    normalization: NormalizationMode = NormalizationMode.LATIN_ASCII_IGNORE,
) -> tuple[NameValueUnit, ...]:
    """Return the per-letter Pythagorean values for ``name``.

    Case is folded and any character outside A-Z is ignored under the default
    compatibility mode. ``LATIN_ACCENT_FOLD`` removes Unicode compatibility
    combining marks and rejects unsupported meaningful characters that remain.

    Args:
        name: The name to evaluate.
        normalization: Latin normalization policy.

    Returns:
        One :class:`NameValueUnit` per A-Z letter, in input order.
    """

    if normalization is NormalizationMode.LATIN_ACCENT_FOLD:
        return _accent_fold_values(name)
    return tuple(
        NameValueUnit(letter, LETTER_VALUES[letter])
        for letter in name.upper()
        if letter in LETTER_VALUES
    )


def _accent_fold_values(name: str) -> tuple[NameValueUnit, ...]:
    normalized = unicodedata.normalize("NFKD", name).upper()
    units: list[NameValueUnit] = []
    for char in normalized:
        if unicodedata.category(char) == "Mn":
            continue
        value = LETTER_VALUES.get(char)
        if value is not None:
            units.append(NameValueUnit(char, value))
        elif is_ignorable(char):
            continue
        else:
            raise ValidationError(
                f"unsupported character for Latin Pythagorean folding: {char!r} (U+{ord(char):04X})"
            )
    return tuple(units)
