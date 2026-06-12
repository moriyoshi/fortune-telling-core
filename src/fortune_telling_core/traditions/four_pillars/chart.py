"""Four Pillars chart casting."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.four_pillars.birth import FourPillarsBirthData
from fortune_telling_core.traditions.four_pillars.deck import FOUR_PILLARS_DECK
from fortune_telling_core.traditions.four_pillars.pillars import PillarSet
from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi
from fortune_telling_core.traditions.four_pillars.spreads import FOUR_PILLARS_SPREAD
from fortune_telling_core.traditions.four_pillars.stems_branches import (
    branch,
    branch_symbol_id,
    stem,
    stem_symbol_id,
)
from fortune_telling_core.traditions.four_pillars.ten_gods import hidden_ten_gods, ten_god


def draw_from_pillars(pillars: PillarSet, birth: FourPillarsBirthData) -> Draw:
    day_stem = ganzhi(pillars.day_index).stem_index
    selections: list[Selection] = []
    _add_pillar(selections, "year", pillars.year_index, day_stem)
    _add_pillar(selections, "month", pillars.month_index, day_stem)
    _add_pillar(
        selections,
        "day",
        pillars.day_index,
        day_stem,
        extra_stem_modifiers={
            "day_master": "true",
            "luck_direction": "forward" if pillars.luck_forward else "backward",
            "luck_start_age": f"{pillars.luck_start_age:.6f}",
            "month_cycle_index": str(pillars.month_index),
            "luck_count": str(birth.luck_count),
            "target_year": str(birth.target_year),
        },
    )
    _add_pillar(selections, "hour", pillars.hour_index, day_stem)
    return Draw(FOUR_PILLARS_DECK.id, FOUR_PILLARS_SPREAD.id, tuple(selections))


def _add_pillar(
    selections: list[Selection],
    pillar: str,
    cycle_index: int,
    day_stem_index: int,
    *,
    extra_stem_modifiers: dict[str, str] | None = None,
) -> None:
    item = ganzhi(cycle_index)
    stem_data = stem(item.stem_index)
    branch_data = branch(item.branch_index)
    stem_modifiers = {
        "pillar": pillar,
        "kind": "stem",
        "cycle_index": str(cycle_index),
        "element": stem_data.element.value,
        "polarity": stem_data.polarity.value,
        "ten_god": "day_master" if pillar == "day" else ten_god(day_stem_index, item.stem_index),
        "cjk": stem_data.cjk,
    }
    if extra_stem_modifiers is not None:
        stem_modifiers.update(extra_stem_modifiers)
    selections.append(Selection(f"{pillar}_stem", stem_symbol_id(item.stem_index), stem_modifiers))
    selections.append(
        Selection(
            f"{pillar}_branch",
            branch_symbol_id(item.branch_index),
            {
                "pillar": pillar,
                "kind": "branch",
                "cycle_index": str(cycle_index),
                "element": branch_data.element.value,
                "polarity": branch_data.polarity.value,
                "animal": branch_data.animal,
                "hidden_stems": ",".join(str(index) for index in branch_data.hidden_stems),
                "hidden_ten_gods": ",".join(hidden_ten_gods(day_stem_index, item.branch_index)),
                "cjk": branch_data.cjk,
            },
        )
    )
