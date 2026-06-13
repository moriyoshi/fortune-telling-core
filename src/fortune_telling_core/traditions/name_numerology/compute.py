"""Pythagorean name-number computation.

The Pythagorean system assigns each letter a value from its alphabet position
modulo nine (A=1 … I=9, J=1 …, R=9, S=1 … Z=8). Three "core numbers" follow:

- Expression (Destiny): all letters of the name.
- Soul Urge (Heart's Desire): the vowels.
- Personality: the consonants.

Each sum is reduced like a Life Path number, preserving the master numbers
11, 22, and 33. Reduction is shared with the birth-date numerology tradition.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_values import latin_pythagorean
from fortune_telling_core.traditions.name_numerology.config import YMode
from fortune_telling_core.traditions.numerology.numbers import reduce_number

_BASE_VOWELS = frozenset("AEIOU")


def _is_vowel(letter: str, y_mode: YMode) -> bool:
    return letter in _BASE_VOWELS or (letter == "Y" and y_mode is YMode.VOWEL)


@dataclass(frozen=True, slots=True)
class NameChart:
    """The three core name numbers."""

    expression: int
    soul_urge: int
    personality: int
    y_mode: YMode


def compute_chart(name: str, y_mode: YMode) -> NameChart:
    """Compute the Expression, Soul Urge, and Personality numbers for a name.

    Args:
        name: The name; non-letters are ignored and case is folded.
        y_mode: Whether Y counts as a vowel.

    Returns:
        The resolved name chart.

    Raises:
        ValidationError: If the name has no letters, no vowels, or no
            consonants under the chosen ``y_mode``.
    """

    units = latin_pythagorean.values(name)
    if not units:
        raise ValidationError("name must contain at least one letter")

    vowels = [unit for unit in units if _is_vowel(unit.char, y_mode)]
    consonants = [unit for unit in units if not _is_vowel(unit.char, y_mode)]
    if not vowels:
        raise ValidationError("name has no vowels for the soul urge number")
    if not consonants:
        raise ValidationError("name has no consonants for the personality number")

    return NameChart(
        expression=reduce_number(sum(unit.value for unit in units)),
        soul_urge=reduce_number(sum(unit.value for unit in vowels)),
        personality=reduce_number(sum(unit.value for unit in consonants)),
        y_mode=y_mode,
    )
