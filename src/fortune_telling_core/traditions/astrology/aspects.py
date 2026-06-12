"""Aspect calculations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from fortune_telling_core.astronomy.position import normalize_degrees


@dataclass(frozen=True, slots=True)
class AspectDef:
    id: str
    name: str
    angle: float
    orb: float


@dataclass(frozen=True, slots=True)
class Aspect:
    first: str
    second: str
    definition: AspectDef
    orb: float

    def render(self) -> str:
        return f"{self.first} {self.definition.name} {self.second} (orb {self.orb:.2f} degrees)"


DEFAULT_ASPECTS: tuple[AspectDef, ...] = (
    AspectDef("conjunction", "conjunct", 0.0, 8.0),
    AspectDef("opposition", "opposes", 180.0, 8.0),
    AspectDef("trine", "trines", 120.0, 6.0),
    AspectDef("square", "squares", 90.0, 6.0),
    AspectDef("sextile", "sextiles", 60.0, 4.0),
)


def angular_distance(first: float, second: float) -> float:
    distance = abs(normalize_degrees(first) - normalize_degrees(second))
    return min(distance, 360.0 - distance)


def compute_aspects(
    longitudes: Mapping[str, float],
    aspect_defs: Sequence[AspectDef] = DEFAULT_ASPECTS,
) -> tuple[Aspect, ...]:
    ids = tuple(longitudes)
    aspects: list[Aspect] = []
    for first_index, first in enumerate(ids):
        for second in ids[first_index + 1 :]:
            if {first, second} == {"north_node", "south_node"}:
                continue
            distance = angular_distance(longitudes[first], longitudes[second])
            for definition in aspect_defs:
                orb = abs(distance - definition.angle)
                if orb <= definition.orb:
                    aspects.append(Aspect(first, second, definition, orb))
                    break
    return tuple(aspects)


def render_aspects(aspects: Sequence[Aspect]) -> str | None:
    if not aspects:
        return None
    rendered = "; ".join(aspect.render() for aspect in aspects)
    return f"Aspects: {rendered}."
