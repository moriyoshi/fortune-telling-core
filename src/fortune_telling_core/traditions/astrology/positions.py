"""Astrological computed position value types."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from fortune_telling_core.astronomy.position import EclipticPosition, normalize_degrees
from fortune_telling_core.errors import ValidationError


@dataclass(frozen=True, slots=True)
class BodyPosition:
    position_id: str
    longitude: float
    speed: float
    house: int

    def __post_init__(self) -> None:
        if not self.position_id:
            raise ValidationError("body position id must not be empty")
        if self.house < 1 or self.house > 12:
            raise ValidationError("house must be in the range 1..12")
        object.__setattr__(self, "longitude", normalize_degrees(float(self.longitude)))
        object.__setattr__(self, "speed", float(self.speed))

    @property
    def retrograde(self) -> bool:
        return self.speed < 0.0


@dataclass(frozen=True, slots=True)
class AnglePosition:
    position_id: str
    longitude: float
    house: int

    def __post_init__(self) -> None:
        if not self.position_id:
            raise ValidationError("angle position id must not be empty")
        if self.house < 1 or self.house > 12:
            raise ValidationError("house must be in the range 1..12")
        object.__setattr__(self, "longitude", normalize_degrees(float(self.longitude)))


@dataclass(frozen=True, slots=True)
class Houses:
    system: str
    cusps: Sequence[float]

    def __post_init__(self) -> None:
        cusps = tuple(normalize_degrees(float(cusp)) for cusp in self.cusps)
        if len(cusps) != 12:
            raise ValidationError("houses must contain 12 cusps")
        object.__setattr__(self, "cusps", cusps)


@dataclass(frozen=True, slots=True)
class ChartPositions:
    longitudes: Mapping[str, float] = field(default_factory=dict)
    houses: Mapping[str, int] = field(default_factory=dict)
    speeds: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "longitudes",
            {key: normalize_degrees(value) for key, value in self.longitudes.items()},
        )
        object.__setattr__(self, "houses", dict(self.houses))
        object.__setattr__(
            self, "speeds", {key: float(value) for key, value in self.speeds.items()}
        )


__all__ = [
    "AnglePosition",
    "BodyPosition",
    "ChartPositions",
    "EclipticPosition",
    "Houses",
    "normalize_degrees",
]
