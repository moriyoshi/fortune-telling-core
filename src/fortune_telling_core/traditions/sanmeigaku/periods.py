"""Sanmeigaku time-varying periods: 大運 (luck cycles) and 年運 (annual).

These reuse the same machinery as the natal chart — the year/luck-pillar
sexagenary 干支 mapped through :func:`main_star` (通変星 → 十大主星) and
:func:`subordinate_star` (十二運 → 十二大従星) relative to the day stem (日干).

* 年運 (annual fortune) — the calendar year's 干支; its stem yields the year's
  主星 and its branch the year's 従星. Direction-independent, so it needs no
  gender.
* 大運 (luck cycles) — ten-year columns advancing (順行) or retreating (逆行)
  from the month pillar, exactly as Four Pillars luck pillars. Direction is
  陽年男・陰年女 → 順行, 陰年男・陽年女 → 逆行 (see
  :func:`fortune_telling_core.traditions.four_pillars.luck.luck_forward`). The
  start age uses the shared 節入りまでの日数 ÷ 3 convention; schools differ on
  the exact 起運 rule, and this is the same one the Four Pillars engine applies.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.luck import LuckPillar, luck_pillars
from fortune_telling_core.traditions.four_pillars.sexagenary import GanZhi, annual_index, ganzhi
from fortune_telling_core.traditions.sanmeigaku.stars import Star, main_star, subordinate_star


@dataclass(frozen=True, slots=True)
class PeriodStars:
    """The 主星 / 従星 pair a sexagenary 干支 yields for a day stem."""

    ganzhi: GanZhi
    main: Star
    subordinate: Star

    @property
    def cjk(self) -> str:
        return self.ganzhi.cjk


@dataclass(frozen=True, slots=True)
class DaiunColumn:
    """A single 大運 ten-year column."""

    index: int
    start_age: float
    stars: PeriodStars


def _stars_for(day_stem_index: int, item: GanZhi) -> PeriodStars:
    return PeriodStars(
        ganzhi=item,
        main=main_star(day_stem_index, item.stem_index),
        subordinate=subordinate_star(day_stem_index, item.branch_index),
    )


def annual_stars(day_stem_index: int, year: int) -> PeriodStars:
    """Return the 年運 主星 / 従星 for ``year`` relative to the day stem."""

    return _stars_for(day_stem_index, ganzhi(annual_index(year)))


def daiun_columns(
    day_stem_index: int,
    month_cycle_index: int,
    *,
    forward: bool,
    start_age: float,
    count: int,
) -> tuple[DaiunColumn, ...]:
    """Return the 大運 columns, each with its 干支 and 主星 / 従星."""

    columns: list[DaiunColumn] = []
    for pillar in _luck(month_cycle_index, forward=forward, start_age=start_age, count=count):
        columns.append(
            DaiunColumn(
                index=pillar.index,
                start_age=pillar.start_age,
                stars=_stars_for(day_stem_index, ganzhi(pillar.cycle_index)),
            )
        )
    return tuple(columns)


def _luck(
    month_cycle_index: int, *, forward: bool, start_age: float, count: int
) -> tuple[LuckPillar, ...]:
    return luck_pillars(month_cycle_index, forward=forward, start_age=start_age, count=count)
