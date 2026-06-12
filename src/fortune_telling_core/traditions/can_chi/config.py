"""Can Chi configuration enums."""

from enum import StrEnum


class DayBoundary(StrEnum):
    """When the Can Chi day pillar rolls over.

    The hour of Tý (rat) spans 23:00-01:00. Under ``LATE_TY`` the 23:00 hour is
    treated as the first hour of the next day, advancing the day pillar; under
    the default ``MIDNIGHT`` the day pillar follows the civil calendar date.
    """

    MIDNIGHT = "midnight"
    LATE_TY = "late_ty"


__all__ = ["DayBoundary"]
