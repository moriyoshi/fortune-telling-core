"""Shared text helpers for name value systems.

These are tradition-agnostic building blocks consumed by the private value
systems under :mod:`fortune_telling_core.traditions._name_values` and by the
tradition engines built on them. See the design note
``.agents/docs/design/non-ascii-name-numerology.md``.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass

from fortune_telling_core.errors import ValidationError


@dataclass(frozen=True, slots=True)
class NameValueUnit:
    """One value-bearing character and the numeric value assigned to it.

    Args:
        char: The normalized character that carries a value.
        value: The numeric value assigned by a value system.
    """

    char: str
    value: int


def strip_combining_marks(text: str) -> str:
    """Drop combining marks (Unicode category ``Mn``) from ``text``.

    The input is decomposed with NFD first so that precomposed accents and
    script-specific points (Hebrew niqqud, Greek/Latin diacritics) decompose
    into a base character plus combining marks before removal.

    Args:
        text: Arbitrary input text.

    Returns:
        ``text`` with combining marks removed.
    """

    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def is_ignorable(char: str) -> bool:
    """Return whether ``char`` is whitespace or punctuation safe to ignore.

    Value systems may skip separators, whitespace, and punctuation when they
    record that choice in provenance. Letters and other value-bearing marks are
    never ignorable and must be handled explicitly.

    Args:
        char: A single character.

    Returns:
        ``True`` when the character is whitespace or punctuation.
    """

    return char.isspace() or unicodedata.category(char).startswith("P")


def format_value_trace(units: Iterable[NameValueUnit]) -> str:
    """Format value units as a compact replay trace such as ``א:1,ב:2``.

    Args:
        units: The value units to serialize.

    Returns:
        A comma-separated ``char:value`` string.
    """

    return ",".join(f"{unit.char}:{unit.value}" for unit in units)


def parse_value_trace(text: str) -> tuple[NameValueUnit, ...]:
    """Parse a compact value trace produced by :func:`format_value_trace`.

    Args:
        text: A comma-separated ``char:value`` string, possibly empty.

    Returns:
        The decoded value units.

    Raises:
        ValidationError: If an entry is malformed or its value is not an integer.
    """

    if not text:
        return ()
    units: list[NameValueUnit] = []
    for part in text.split(","):
        char, sep, raw_value = part.partition(":")
        if not sep or not char:
            raise ValidationError(f"malformed value-trace entry: {part!r}")
        try:
            value = int(raw_value)
        except ValueError as exc:
            raise ValidationError(f"value-trace value must be an integer: {part!r}") from exc
        units.append(NameValueUnit(char, value))
    return tuple(units)
