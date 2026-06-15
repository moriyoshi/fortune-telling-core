"""Koyomi (暦注) day-quality calculations.

All computations are deterministic functions of a civil instant:

* 六曜 (rokuyō) from the lunisolar month and day.
* The day's sexagenary 干支 from the day count.
* 一粒万倍日, 三隣亡, and 天赦日 from the sectional solar month (節月) and the
  day's stem/branch.

The annotations that lacked a single authoritative public definition when this
module was written — 不成就日 (sources disagree on the day pattern) and the
calendrical 二十八宿 cycle (no verifiable epoch anchor) — are intentionally
omitted rather than guessed.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.sexagenary import GanZhi

# Rokuyō by ``(lunar_month + lunar_day) % 6``. Lunar 1/1 is 先勝, fixing the map.
ROKUYO: tuple[tuple[str, str, str], ...] = (
    ("taian", "大安", "Taian"),  # 0
    ("shakko", "赤口", "Shakko"),  # 1
    ("sensho", "先勝", "Sensho"),  # 2
    ("tomobiki", "友引", "Tomobiki"),  # 3
    ("sembu", "先負", "Sembu"),  # 4
    ("butsumetsu", "仏滅", "Butsumetsu"),  # 5
)

# 一粒万倍日: the two day branches per sectional month (節月), indexed 0=正月 (寅月)
# … 11=十二月 (丑月). Standard koyomi8 "Method I" table. Branch indices are
# 子=0 … 亥=11.
_ICHIRYU_MANBAI: tuple[tuple[int, int], ...] = (
    (1, 6),  # 正月: 丑・午
    (9, 2),  # 二月: 酉・寅
    (0, 3),  # 三月: 子・卯
    (3, 4),  # 四月: 卯・辰
    (5, 6),  # 五月: 巳・午
    (6, 9),  # 六月: 午・酉
    (0, 7),  # 七月: 子・未
    (3, 8),  # 八月: 卯・申
    (6, 9),  # 九月: 午・酉
    (9, 10),  # 十月: 酉・戌
    (11, 0),  # 十一月: 亥・子
    (0, 3),  # 十二月: 子・卯
)

# 三隣亡 forbidden day branch by sectional month group (節月 index % 3).
_SANRINBO_BRANCH: tuple[int, int, int] = (11, 2, 6)  # 亥, 寅, 午

# 天赦日: the day's full 干支 by season. Spring 戊寅, summer 甲午, autumn 戊申,
# winter 甲子. Seasons follow the sectional months (0-2 spring … 9-11 winter).
_TENSHA_GANZHI: tuple[str, str, str, str] = ("戊寅", "甲午", "戊申", "甲子")


@dataclass(frozen=True, slots=True)
class DayNotes:
    """Computed koyomi annotations for one civil day."""

    rokuyo_index: int
    sekki_month: int  # 1..12 (節月)
    is_ichiryu_manbai: bool
    is_sanrinbo: bool
    is_tensha: bool


def rokuyo_index(lunar_month: int, lunar_day: int) -> int:
    """Return the rokuyō index from a lunisolar month and day."""

    return (lunar_month + lunar_day) % 6


def is_ichiryu_manbai(sekki_month_index: int, day_branch: int) -> bool:
    """Whether the day is 一粒万倍日 for a sectional-month index (0=正月)."""

    return day_branch in _ICHIRYU_MANBAI[sekki_month_index]


def is_sanrinbo(sekki_month_index: int, day_branch: int) -> bool:
    """Whether the day is 三隣亡 for a sectional-month index (0=正月)."""

    return day_branch == _SANRINBO_BRANCH[sekki_month_index % 3]


def is_tensha(sekki_month_index: int, day: GanZhi) -> bool:
    """Whether the day is 天赦日 for a sectional-month index (0=正月)."""

    return day.cjk == _TENSHA_GANZHI[sekki_month_index // 3]


def compute_day_notes(
    sekki_month_index: int, lunar_month: int, lunar_day: int, day: GanZhi
) -> DayNotes:
    """Compute all supported koyomi annotations for a day."""

    return DayNotes(
        rokuyo_index=rokuyo_index(lunar_month, lunar_day),
        sekki_month=sekki_month_index + 1,
        is_ichiryu_manbai=is_ichiryu_manbai(sekki_month_index, day.branch_index),
        is_sanrinbo=is_sanrinbo(sekki_month_index, day.branch_index),
        is_tensha=is_tensha(sekki_month_index, day),
    )
