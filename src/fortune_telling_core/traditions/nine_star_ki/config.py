"""Nine Star Ki configuration choices."""

from enum import StrEnum


class DayStarEscapement(StrEnum):
    """Daily-star solstice reversal schools.

    ``JIAZI_AT_OR_BEFORE_SOLSTICE`` is this package's compatibility default:
    the active winter or summer solstice is rounded to a civil day, then the
    nearest preceding Jia-Zi day is assigned Star 1 for the forward arc or
    Star 9 for the backward arc.

    ``FIRST_JIAZI_AFTER_SOLSTICE`` follows a documented Daily Flying Star
    convention in which Star 1 or Star 9 presides on the first Jia-Zi day
    after the relevant solstice. See the "Daily Flying Star" rules cited on
    https://en.wikipedia.org/wiki/Flying_Star_Feng_Shui.
    """

    JIAZI_AT_OR_BEFORE_SOLSTICE = "jiazi_at_or_before_solstice"
    FIRST_JIAZI_AFTER_SOLSTICE = "first_jiazi_after_solstice"
