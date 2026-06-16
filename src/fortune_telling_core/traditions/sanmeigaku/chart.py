"""Sanmeigaku chart casting."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
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


def draw_from_pillars(
    pillars: PillarSet,
    *,
    target_year: int,
    gender: LuckDirectionInput | None,
    luck_count: int,
) -> Draw:
    """Build a Sanmeigaku draw from the year, month, and day pillars.

    The center (``day_branch``) selection also carries the inputs needed to
    re-derive the time-varying 年運 and 大運 from the draw alone, so a replay
    reproduces them without touching the ephemeris.
    """

    year = ganzhi(pillars.year_index)
    month = ganzhi(pillars.month_index)
    day = ganzhi(pillars.day_index)
    day_stem = day.stem_index
    day_stem_cjk = stem(day_stem).cjk

    centre_meta: dict[str, str] = {
        "day_stem_index": str(day_stem),
        "month_cycle_index": str(pillars.month_index),
        "target_year": str(target_year),
    }
    if gender is not None:
        centre_meta.update(
            {
                "gender": gender.value,
                "luck_direction": "forward" if pillars.luck_forward else "backward",
                "luck_start_age": f"{pillars.luck_start_age:.6f}",
                "luck_count": str(luck_count),
            }
        )

    selections: list[Selection] = []

    def main(
        position: str,
        source_stem_index: int,
        source_cjk: str,
        *,
        extra: dict[str, str] | None = None,
    ) -> None:
        star = main_star(day_stem, source_stem_index)
        modifiers = {
            "kind": "main_star",
            "star_cjk": star.cjk,
            "source": source_cjk,
            "ten_god": ten_god(day_stem, source_stem_index),
            "day_master": day_stem_cjk,
        }
        if extra is not None:
            modifiers.update(extra)
        selections.append(Selection(position, f"sanmeigaku.main.{star.slug}", modifiers))

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
    main(
        "day_branch",
        _principal_hidden_stem(day.branch_index),
        branch(day.branch_index).cjk,
        extra=centre_meta,
    )
    subordinate("year_branch_subordinate", year.branch_index)
    subordinate("month_branch_subordinate", month.branch_index)
    subordinate("day_branch_subordinate", day.branch_index)

    return Draw(SANMEIGAKU_DECK.id, SANMEIGAKU_SPREAD.id, tuple(selections))
