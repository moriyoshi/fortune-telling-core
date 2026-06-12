"""Nine Star Ki chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.nine_star_ki.deck import NINE_STAR_KI_DECK
from fortune_telling_core.traditions.nine_star_ki.lo_shu import fly_chart, render_chart
from fortune_telling_core.traditions.nine_star_ki.spreads import NINE_STAR_KI_SPREAD
from fortune_telling_core.traditions.nine_star_ki.star_calc import NineStarKiChart
from fortune_telling_core.traditions.nine_star_ki.stars import star


def draw_from_chart(chart: NineStarKiChart) -> Draw:
    common = {
        "solar_year": str(chart.solar_year),
        "year_star": str(chart.year_star),
        "target_year": str(chart.target_year),
        "annual_star": str(chart.annual_star),
        "solar_month_index": str(chart.solar_month_index),
        "month_star": str(chart.month_star),
        "day_star": str(chart.day_star),
        "direction": chart.day_direction,
        "day_star_escapement": chart.day_star_escapement.value,
        "tendency_star": str(chart.tendency_star),
        "center_case": "true" if chart.center_case else "false",
        "annual_chart": render_chart(fly_chart(chart.annual_star)),
        "monthly_chart": render_chart(fly_chart(chart.month_star)),
    }
    selections = (
        _selection("principal", chart.year_star, common),
        _selection("monthly", chart.month_star, common),
        _selection("daily", chart.day_star, common),
        _selection("tendency", chart.tendency_star, common),
    )
    return Draw(NINE_STAR_KI_DECK.id, NINE_STAR_KI_SPREAD.id, selections)


def _selection(position_id: str, number: int, common: dict[str, str]) -> Selection:
    data = star(number)
    return Selection(
        position_id,
        data.symbol_id,
        {
            **common,
            "role": position_id,
            "number": str(data.number),
            "element": data.element,
            "trigram": data.trigram,
            "color": data.color,
            "cjk": data.cjk,
            "home_palace": data.home_palace,
        },
    )
