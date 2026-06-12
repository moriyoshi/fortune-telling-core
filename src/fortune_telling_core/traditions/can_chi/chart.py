"""Can Chi chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.can_chi.config import DayBoundary
from fortune_telling_core.traditions.can_chi.deck import CAN_CHI_DECK
from fortune_telling_core.traditions.can_chi.pillars import CanChiChart, Pillar
from fortune_telling_core.traditions.can_chi.spreads import CAN_CHI_SPREAD
from fortune_telling_core.traditions.can_chi.stems_branches import can, chi


def _pillar_name(pillar: Pillar) -> str:
    return f"{can(pillar.can_index).name} {chi(pillar.chi_index).name}"


def draw_from_chart(chart: CanChiChart, day_boundary: DayBoundary) -> Draw:
    common = {
        "day_pillar": _pillar_name(chart.day),
        "hour_pillar": _pillar_name(chart.hour),
        "day_boundary": day_boundary.value,
    }
    selections = (
        _can_selection("day_can", chart.day, common),
        _chi_selection("day_chi", chart.day, common),
        _can_selection("hour_can", chart.hour, common),
        _chi_selection("hour_chi", chart.hour, common),
    )
    return Draw(CAN_CHI_DECK.id, CAN_CHI_SPREAD.id, selections)


def _can_selection(position_id: str, pillar: Pillar, common: dict[str, str]) -> Selection:
    data = can(pillar.can_index)
    return Selection(
        position_id,
        data.symbol_id,
        {
            **common,
            "role": position_id,
            "cycle_index": str(data.index),
            "element": data.element,
            "polarity": data.polarity,
        },
    )


def _chi_selection(position_id: str, pillar: Pillar, common: dict[str, str]) -> Selection:
    data = chi(pillar.chi_index)
    return Selection(
        position_id,
        data.symbol_id,
        {
            **common,
            "role": position_id,
            "cycle_index": str(data.index),
            "animal": data.animal,
            "animal_vi": data.animal_vi,
            "element": data.element,
            "polarity": data.polarity,
        },
    )
