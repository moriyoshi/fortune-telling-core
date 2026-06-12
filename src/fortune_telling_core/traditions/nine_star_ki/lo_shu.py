"""Lo Shu flying-star chart helpers."""

from __future__ import annotations

from fortune_telling_core.traditions.nine_star_ki.stars import HOME_PALACE

PALACES: tuple[str, ...] = ("N", "NE", "E", "SE", "C", "SW", "W", "NW", "S")
FLIGHT_ORDER: tuple[str, ...] = ("C", "NW", "W", "NE", "S", "N", "SW", "E", "SE")
LO_SHU_BASE: dict[str, int] = {palace: star for star, palace in HOME_PALACE.items()}


def fly_chart(center: int) -> dict[str, int]:
    return {palace: _wrap_star(center + index) for index, palace in enumerate(FLIGHT_ORDER)}


def render_chart(chart: dict[str, int]) -> str:
    return (
        f"NW:{chart['NW']} N:{chart['N']} NE:{chart['NE']} / "
        f"W:{chart['W']} C:{chart['C']} E:{chart['E']} / "
        f"SW:{chart['SW']} S:{chart['S']} SE:{chart['SE']}"
    )


def _wrap_star(value: int) -> int:
    return ((value - 1) % 9) + 1
