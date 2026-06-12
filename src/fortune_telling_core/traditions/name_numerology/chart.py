"""Name numerology chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.name_numerology.compute import NameChart
from fortune_telling_core.traditions.name_numerology.deck import NAME_NUMEROLOGY_DECK
from fortune_telling_core.traditions.name_numerology.spreads import NAME_NUMEROLOGY_SPREAD
from fortune_telling_core.traditions.numerology.numbers import number


def draw_from_chart(chart: NameChart) -> Draw:
    common = {
        "expression": str(chart.expression),
        "soul_urge": str(chart.soul_urge),
        "personality": str(chart.personality),
        "y_mode": chart.y_mode.value,
    }
    selections = (
        _selection("expression", chart.expression, common),
        _selection("soul_urge", chart.soul_urge, common),
        _selection("personality", chart.personality, common),
    )
    return Draw(NAME_NUMEROLOGY_DECK.id, NAME_NUMEROLOGY_SPREAD.id, selections)


def _selection(position_id: str, value: int, common: dict[str, str]) -> Selection:
    data = number(value)
    return Selection(
        position_id,
        f"name_numerology.number.{value}",
        {
            **common,
            "role": position_id,
            "value": str(data.value),
            "keyword": data.keyword,
            "master": "true" if data.master else "false",
        },
    )
