"""Numerology chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.numerology.deck import NUMEROLOGY_DECK
from fortune_telling_core.traditions.numerology.numbers import NumerologyChart, number
from fortune_telling_core.traditions.numerology.spreads import NUMEROLOGY_SPREAD


def draw_from_chart(chart: NumerologyChart) -> Draw:
    common = {
        "life_path": str(chart.life_path),
        "birthday": str(chart.birthday),
        "reduction_method": chart.method.value,
    }
    selections = (
        _selection("life_path", chart.life_path, common),
        _selection("birthday", chart.birthday, common),
    )
    return Draw(NUMEROLOGY_DECK.id, NUMEROLOGY_SPREAD.id, selections)


def _selection(position_id: str, value: int, common: dict[str, str]) -> Selection:
    data = number(value)
    return Selection(
        position_id,
        data.symbol_id,
        {
            **common,
            "role": position_id,
            "value": str(data.value),
            "keyword": data.keyword,
            "master": "true" if data.master else "false",
        },
    )
