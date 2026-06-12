"""Four Pillars configuration enums."""

from enum import StrEnum

from fortune_telling_core.astronomy.time_model import TimeModel


class Element(StrEnum):
    WOOD = "wood"
    FIRE = "fire"
    EARTH = "earth"
    METAL = "metal"
    WATER = "water"


class Polarity(StrEnum):
    YANG = "yang"
    YIN = "yin"


class DayBoundary(StrEnum):
    MIDNIGHT = "midnight"
    LATE_ZISHI = "late_zishi"


class LuckDirectionInput(StrEnum):
    MALE = "male"
    FEMALE = "female"


__all__ = [
    "DayBoundary",
    "Element",
    "LuckDirectionInput",
    "Polarity",
    "TimeModel",
]
