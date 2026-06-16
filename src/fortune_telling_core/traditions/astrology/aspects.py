"""Aspect calculations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from fortune_telling_core.astronomy.position import normalize_degrees
from fortune_telling_core.draw import Selection

# Symbol id prefix for a structured aspect, e.g. ``astro.aspect.trine``. The
# interpretation layer keys localized text off the full symbol id plus the
# ``kind`` modifier (natal vs transit).
ASPECT_SYMBOL_PREFIX = "astro.aspect."


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


def compute_cross_aspects(
    transit: Mapping[str, float],
    natal: Mapping[str, float],
    aspect_defs: Sequence[AspectDef] = DEFAULT_ASPECTS,
) -> tuple[Aspect, ...]:
    """Aspects between two bodies of positions (e.g. transiting vs natal).

    Unlike :func:`compute_aspects`, every transit position is tested against
    every natal position (a full cross product), since the two maps describe
    different charts rather than one.
    """

    aspects: list[Aspect] = []
    for first, first_longitude in transit.items():
        for second, second_longitude in natal.items():
            distance = angular_distance(first_longitude, second_longitude)
            for definition in aspect_defs:
                orb = abs(distance - definition.angle)
                if orb <= definition.orb:
                    aspects.append(Aspect(first, second, definition, orb))
                    break
    return tuple(aspects)


def render_aspects(aspects: Sequence[Aspect], *, heading: str = "Aspects") -> str | None:
    if not aspects:
        return None
    rendered = "; ".join(aspect.render() for aspect in aspects)
    return f"{heading}: {rendered}."


def aspect_selection(aspect: Aspect, kind: str) -> Selection:
    """Render an aspect as a structured, position-free draw selection.

    Args:
        aspect: The computed aspect.
        kind: ``"natal"`` or ``"transit"`` — for transit aspects ``first`` is
            the transiting body and ``second`` the natal body.

    Returns:
        A :class:`Selection` with ``symbol_id`` ``astro.aspect.<type>`` and
        modifiers ``first`` / ``second`` (body ids), ``orb``, and ``kind``.
    """

    return Selection(
        position_id="aspect",
        symbol_id=f"{ASPECT_SYMBOL_PREFIX}{aspect.definition.id}",
        modifiers={
            "first": aspect.first,
            "second": aspect.second,
            "orb": f"{aspect.orb:.2f}",
            "kind": kind,
        },
    )


def aspect_extras(
    natal: Mapping[str, float],
    transit: Mapping[str, float] | None = None,
) -> tuple[Selection, ...]:
    """Structured aspect selections for a chart.

    Natal aspects (within ``natal``) are always produced; transit-to-natal
    cross-aspects are added when ``transit`` is given (``request.as_of`` set).
    """

    extras = [aspect_selection(aspect, "natal") for aspect in compute_aspects(natal)]
    if transit is not None:
        extras.extend(
            aspect_selection(aspect, "transit") for aspect in compute_cross_aspects(transit, natal)
        )
    return tuple(extras)
