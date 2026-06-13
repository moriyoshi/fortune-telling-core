"""Chaldean numerology letter values, planetary rulers, and name computation.

The Chaldean system differs from the Pythagorean one in two ways: letters take
values 1-8 only (nine was held sacred and never assigned to a letter), and the
single-digit root carries a planetary ruler. A name's letters are summed and the
total reduced to a root from 1 to 9.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_values import latin_chaldean

_LETTER_VALUES = latin_chaldean.LETTER_VALUES

# Planetary rulers of the single-digit roots (Cheiro's Chaldean system).
_PLANETS = {
    1: "Sun",
    2: "Moon",
    3: "Jupiter",
    4: "Uranus",
    5: "Mercury",
    6: "Venus",
    7: "Neptune",
    8: "Saturn",
    9: "Mars",
}


@dataclass(frozen=True, slots=True)
class ChaldeanNumber:
    """A single-digit Chaldean root and its planetary ruler."""

    value: int
    planet: str

    @property
    def symbol_id(self) -> str:
        return f"chaldean_numerology.number.{self.value}"


NUMBERS: tuple[ChaldeanNumber, ...] = tuple(
    ChaldeanNumber(value, planet) for value, planet in _PLANETS.items()
)

NUMBER_BY_VALUE = {item.value: item for item in NUMBERS}


def number(value: int) -> ChaldeanNumber:
    """Return the Chaldean number for a root value."""

    return NUMBER_BY_VALUE[value]


def reduce_to_root(total: int) -> int:
    """Reduce a sum to a single digit from 1 to 9 (no master numbers)."""

    while total > 9:
        total = sum(int(digit) for digit in str(total))
    return total


@dataclass(frozen=True, slots=True)
class NameNumber:
    """A resolved Chaldean name number."""

    total: int
    root: int


def compute_name_number(name: str) -> NameNumber:
    """Compute the Chaldean name number.

    Args:
        name: The name; non-letters are ignored and case is folded.

    Returns:
        The letter-sum total and its reduced root.

    Raises:
        ValidationError: If the name has no Chaldean letters.
    """

    units = latin_chaldean.values(name)
    total = latin_chaldean.total(units)
    if total == 0:
        raise ValidationError("name must contain at least one letter")
    return NameNumber(total=total, root=reduce_to_root(total))
