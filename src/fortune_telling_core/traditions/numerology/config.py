"""Numerology configuration enums."""

from enum import StrEnum


class ReductionMethod(StrEnum):
    """How the Life Path number is reduced from the birth date.

    The two widely taught methods diverge only when a master number (11, 22, 33)
    appears in a component:

    - ``COMPONENT`` reduces the month, day, and year separately — each able to
      surface a master number — then sums and reduces the result. This is the
      method most numerologists consider correct, and the default.
    - ``ITERATIVE`` sums every digit of the whole date at once, then reduces.
      Simpler, but it can dissolve a master number that ``COMPONENT`` preserves.
    """

    COMPONENT = "component"
    ITERATIVE = "iterative"


__all__ = ["ReductionMethod"]
