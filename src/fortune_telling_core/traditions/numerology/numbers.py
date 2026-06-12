"""Pythagorean numerology number data and birth-date computation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from fortune_telling_core.traditions.numerology.config import ReductionMethod

MASTER_NUMBERS = frozenset({11, 22, 33})


@dataclass(frozen=True, slots=True)
class NumerologyNumber:
    """A reduced numerology number with its keyword."""

    value: int
    keyword: str

    @property
    def master(self) -> bool:
        return self.value in MASTER_NUMBERS

    @property
    def symbol_id(self) -> str:
        return f"numerology.number.{self.value}"


NUMBERS: tuple[NumerologyNumber, ...] = (
    NumerologyNumber(1, "Leader"),
    NumerologyNumber(2, "Diplomat"),
    NumerologyNumber(3, "Communicator"),
    NumerologyNumber(4, "Builder"),
    NumerologyNumber(5, "Freedom"),
    NumerologyNumber(6, "Nurturer"),
    NumerologyNumber(7, "Seeker"),
    NumerologyNumber(8, "Power"),
    NumerologyNumber(9, "Humanitarian"),
    NumerologyNumber(11, "Inspirer"),
    NumerologyNumber(22, "Master Builder"),
    NumerologyNumber(33, "Master Teacher"),
)

NUMBER_BY_VALUE = {item.value: item for item in NUMBERS}


def number(value: int) -> NumerologyNumber:
    """Return the numerology number for a reduced value."""

    return NUMBER_BY_VALUE[value]


def reduce_number(value: int) -> int:
    """Reduce a positive integer to a single digit, preserving master numbers."""

    while value > 9 and value not in MASTER_NUMBERS:
        value = sum(int(digit) for digit in str(value))
    return value


def _digit_sum(value: int) -> int:
    return sum(int(digit) for digit in str(value))


@dataclass(frozen=True, slots=True)
class NumerologyChart:
    """A resolved numerology chart derived from a birth date."""

    life_path: int
    birthday: int
    method: ReductionMethod


def compute_chart(day: date, method: ReductionMethod) -> NumerologyChart:
    """Compute the Life Path and Birthday numbers for a birth date.

    Args:
        day: Gregorian birth date.
        method: How to reduce the Life Path number (see ``ReductionMethod``).

    Returns:
        The resolved numerology chart.
    """

    if method is ReductionMethod.COMPONENT:
        life_path = reduce_number(
            reduce_number(day.month) + reduce_number(day.day) + reduce_number(day.year)
        )
    else:
        life_path = reduce_number(
            _digit_sum(day.year) + _digit_sum(day.month) + _digit_sum(day.day)
        )
    return NumerologyChart(life_path=life_path, birthday=reduce_number(day.day), method=method)
