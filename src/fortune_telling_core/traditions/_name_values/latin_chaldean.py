"""Latin Chaldean letter-value system."""

from __future__ import annotations

from fortune_telling_core.traditions._name_text import NameValueUnit

ID = "latin_chaldean.v1"
VERSION = "1"

GROUPS = {
    1: "AIJQY",
    2: "BKR",
    3: "CGLS",
    4: "DMT",
    5: "EHNX",
    6: "UVW",
    7: "OZ",
    8: "FP",
}

LETTER_VALUES = {letter: value for value, letters in GROUPS.items() for letter in letters}


def values(name: str) -> tuple[NameValueUnit, ...]:
    """Return the per-letter Chaldean values for ``name``.

    Case is folded and any character outside A-Z is ignored to preserve the
    existing Chaldean numerology behavior.
    """

    return tuple(
        NameValueUnit(letter, LETTER_VALUES[letter])
        for letter in name.upper()
        if letter in LETTER_VALUES
    )


def total(units: tuple[NameValueUnit, ...]) -> int:
    """Return the sum of the values in ``units``."""

    return sum(unit.value for unit in units)
