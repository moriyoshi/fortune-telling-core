"""Sanmeigaku configuration enums."""

from enum import StrEnum

from fortune_telling_core.astronomy.time_model import TimeModel
from fortune_telling_core.traditions.four_pillars.config import DayBoundary


class HiddenStemRule(StrEnum):
    """Principal hidden-stem (元命) selection rule.

    ``PRIMARY`` selects each branch's principal qi (本気) — the first hidden
    stem recorded for the branch. This is a deterministic, reproducible
    default.

    The classical 月律分野 rule selects the 元命 from the days elapsed since
    the sectional solar term (節入り), choosing 余気 / 中気 / 本気 by
    documented day thresholds. Those thresholds diverge between schools and no
    single authoritative public table was available when this engine was
    written, so the day-threshold rule is intentionally not bundled. Register
    a future value here once a sourced table is available.
    """

    PRIMARY = "primary"


__all__ = [
    "DayBoundary",
    "HiddenStemRule",
    "TimeModel",
]
