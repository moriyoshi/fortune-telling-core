"""Sanmeigaku chart casting."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.four_pillars.pillars import PillarSet
from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi
from fortune_telling_core.traditions.four_pillars.stems_branches import branch, stem
from fortune_telling_core.traditions.four_pillars.ten_gods import ten_god
from fortune_telling_core.traditions.sanmeigaku.deck import SANMEIGAKU_DECK
from fortune_telling_core.traditions.sanmeigaku.spreads import SANMEIGAKU_SPREAD
from fortune_telling_core.traditions.sanmeigaku.stars import (
    life_stage_slug,
    main_star,
    subordinate_star,
)


def _principal_hidden_stem(branch_index: int) -> int:
    """Return a branch's principal qi (本気) hidden-stem index."""

    return branch(branch_index).hidden_stems[0]


def draw_from_pillars(pillars: PillarSet) -> Draw:
    """Build a Sanmeigaku draw from the year, month, and day pillars."""

    year = ganzhi(pillars.year_index)
    month = ganzhi(pillars.month_index)
    day = ganzhi(pillars.day_index)
    day_stem = day.stem_index
    day_stem_cjk = stem(day_stem).cjk

    selections: list[Selection] = []

    def main(position: str, source_stem_index: int, source_cjk: str) -> None:
        star = main_star(day_stem, source_stem_index)
        selections.append(
            Selection(
                position,
                f"sanmeigaku.main.{star.slug}",
                {
                    "kind": "main_star",
                    "star_cjk": star.cjk,
                    "source": source_cjk,
                    "ten_god": ten_god(day_stem, source_stem_index),
                    "day_master": day_stem_cjk,
                },
            )
        )

    def subordinate(position: str, branch_index: int) -> None:
        star = subordinate_star(day_stem, branch_index)
        selections.append(
            Selection(
                position,
                f"sanmeigaku.subordinate.{star.slug}",
                {
                    "kind": "subordinate_star",
                    "star_cjk": star.cjk,
                    "source": branch(branch_index).cjk,
                    "life_stage": life_stage_slug(day_stem, branch_index),
                    "day_master": day_stem_cjk,
                },
            )
        )

    main("year_stem", year.stem_index, stem(year.stem_index).cjk)
    main("month_stem", month.stem_index, stem(month.stem_index).cjk)
    main("year_branch", _principal_hidden_stem(year.branch_index), branch(year.branch_index).cjk)
    main("month_branch", _principal_hidden_stem(month.branch_index), branch(month.branch_index).cjk)
    main("day_branch", _principal_hidden_stem(day.branch_index), branch(day.branch_index).cjk)
    subordinate("year_branch_subordinate", year.branch_index)
    subordinate("month_branch_subordinate", month.branch_index)
    subordinate("day_branch_subordinate", day.branch_index)

    return Draw(SANMEIGAKU_DECK.id, SANMEIGAKU_SPREAD.id, tuple(selections))
