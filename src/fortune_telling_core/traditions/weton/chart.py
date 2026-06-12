"""Weton chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.weton.calendar import WetonChart
from fortune_telling_core.traditions.weton.config import DayBoundary
from fortune_telling_core.traditions.weton.deck import WETON_DECK
from fortune_telling_core.traditions.weton.spreads import WETON_SPREAD


def draw_from_chart(chart: WetonChart, day_boundary: DayBoundary) -> Draw:
    common = {
        "weton": chart.name,
        "neptu": str(chart.neptu),
        "day_boundary": day_boundary.value,
    }
    selections = (
        Selection(
            "saptawara",
            chart.saptawara.symbol_id,
            {
                **common,
                "role": "saptawara",
                "slug": chart.saptawara.slug,
                "javanese": chart.saptawara.javanese,
                "weekday": str(chart.saptawara.weekday),
                "day_neptu": str(chart.saptawara.neptu),
            },
        ),
        Selection(
            "pancawara",
            chart.pancawara.symbol_id,
            {
                **common,
                "role": "pancawara",
                "slug": chart.pancawara.slug,
                "javanese": chart.pancawara.javanese,
                "index": str(chart.pancawara.index),
                "pasaran_neptu": str(chart.pancawara.neptu),
            },
        ),
    )
    return Draw(WETON_DECK.id, WETON_SPREAD.id, selections)
