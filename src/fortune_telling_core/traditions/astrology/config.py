"""Astrology chart configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from fortune_telling_core.errors import ValidationError


class ZodiacMode(StrEnum):
    TROPICAL = "tropical"
    SIDEREAL = "sidereal"


class Ayanamsa(StrEnum):
    LAHIRI = "lahiri"


class HouseSystem(StrEnum):
    WHOLE_SIGN = "whole_sign"
    EQUAL = "equal"
    PLACIDUS = "placidus"


@dataclass(frozen=True, slots=True)
class ChartConfig:
    zodiac: ZodiacMode = ZodiacMode.TROPICAL
    ayanamsa: Ayanamsa | None = None
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN
    high_latitude_fallback: bool = False
    include_angles_in_aspects: bool = True

    def __post_init__(self) -> None:
        if self.zodiac == ZodiacMode.SIDEREAL and self.ayanamsa is None:
            raise ValidationError("sidereal charts require an ayanamsa")
