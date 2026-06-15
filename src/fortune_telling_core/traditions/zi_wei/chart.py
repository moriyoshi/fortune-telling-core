"""Zi Wei Dou Shu (紫微斗数) chart computation.

Deterministic placement of the twelve palaces and the fourteen major stars from
a lunisolar birth date and the birth double-hour. Every rule here is the
standard one used across schools for *major-star* placement:

* 命宮 / 身宮 from the lunar month and birth-hour branch.
* Palace heavenly stems by the 五虎遁 rule from the year stem.
* 五行局 (Five-Element Bureau) from the 納音 element of the 命宮 stem-branch.
* 紫微 from the bureau and lunar day (the 起紫微 quotient/remainder/parity rule).
* The 紫微 and 天府 series at fixed offsets, with 天府 the reflection of 紫微
  across the 寅–申 axis.

Minor stars and the 四化 transformations (which reference stars outside the
fourteen majors and diverge between schools) are intentionally not computed.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.sexagenary import annual_index, index_for

BRANCH_CJK: tuple[str, ...] = (
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
)
BRANCH_SLUG: tuple[str, ...] = (
    "zi", "chou", "yin", "mao", "chen", "si", "wu", "wei", "shen", "you", "xu", "hai",
)
STEM_CJK: tuple[str, ...] = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")

# The twelve palaces in placement order (命宮 first), assigned to branches going
# backward (逆) around the wheel.
PALACES: tuple[tuple[str, str], ...] = (
    ("ming", "命宮"),
    ("siblings", "兄弟宮"),
    ("spouse", "夫妻宮"),
    ("children", "子女宮"),
    ("wealth", "財帛宮"),
    ("health", "疾厄宮"),
    ("travel", "遷移宮"),
    ("friends", "僕役宮"),
    ("career", "官祿宮"),
    ("property", "田宅宮"),
    ("fortune", "福德宮"),
    ("parents", "父母宮"),
)


@dataclass(frozen=True, slots=True)
class Star:
    slug: str
    cjk: str


# 紫微 series offsets are counted backward from 紫微; 天府 series forward from 天府.
_ZIWEI_SERIES: tuple[tuple[Star, int], ...] = (
    (Star("ziwei", "紫微"), 0),
    (Star("tianji", "天機"), -1),
    (Star("taiyang", "太陽"), -3),
    (Star("wuqu", "武曲"), -4),
    (Star("tiantong", "天同"), -5),
    (Star("lianzhen", "廉貞"), -8),
)
_TIANFU_SERIES: tuple[tuple[Star, int], ...] = (
    (Star("tianfu", "天府"), 0),
    (Star("taiyin", "太陰"), 1),
    (Star("tanlang", "貪狼"), 2),
    (Star("jumen", "巨門"), 3),
    (Star("tianxiang", "天相"), 4),
    (Star("tianliang", "天梁"), 5),
    (Star("qisha", "七殺"), 6),
    (Star("pojun", "破軍"), 10),
)
MAJOR_STARS: tuple[Star, ...] = tuple(star for star, _ in _ZIWEI_SERIES) + tuple(
    star for star, _ in _TIANFU_SERIES
)

# 納音 element bureau number by sexagenary pair (index // 2): 水2 木3 金4 土5 火6.
# Derived from the classic 六十甲子納音 (海中金 … 大海水).
_NAYIN_BUREAU: tuple[int, ...] = (
    4, 6, 3, 5, 4, 6, 2, 5, 4, 3, 2, 5, 6, 3, 2, 4, 6, 3, 5, 4,
    6, 2, 5, 4, 3, 2, 5, 6, 3, 2,
)


@dataclass(frozen=True, slots=True)
class ZiWeiChart:
    ming_branch: int
    body_branch: int
    bureau: int
    ziwei_branch: int
    tianfu_branch: int
    palace_branches: tuple[int, ...]  # branch per palace, in PALACES order
    palace_stems: tuple[int, ...]  # stem index per palace
    stars_by_branch: tuple[tuple[Star, ...], ...]  # stars on each branch 0..11
    year_stem: int
    year_branch: int


def _yin_palace_stem(year_stem: int) -> int:
    """Stem index on the 寅 palace by the 五虎遁 rule."""

    return (year_stem * 2 + 2) % 10


def _palace_stem(year_stem: int, branch: int) -> int:
    return (_yin_palace_stem(year_stem) + (branch - 2) % 12) % 10


def _bureau(year_stem: int, ming_branch: int) -> int:
    stem = _palace_stem(year_stem, ming_branch)
    return _NAYIN_BUREAU[index_for(stem, ming_branch) // 2]


def _ziwei_branch(bureau: int, lunar_day: int) -> int:
    quotient = -(-lunar_day // bureau)  # ceil division
    remainder = quotient * bureau - lunar_day
    step = quotient + remainder if remainder % 2 == 0 else quotient - remainder
    return (1 + step) % 12


def compute_chart(
    lunar_year: int, lunar_month: int, lunar_day: int, hour_branch: int
) -> ZiWeiChart:
    """Compute a Zi Wei chart from lunar date components and the hour branch."""

    year_gz = annual_index(lunar_year)
    year_stem = year_gz % 10
    year_branch = year_gz % 12

    month_palace = (1 + lunar_month) % 12
    ming_branch = (month_palace - hour_branch) % 12
    body_branch = (month_palace + hour_branch) % 12

    bureau = _bureau(year_stem, ming_branch)
    ziwei_branch = _ziwei_branch(bureau, lunar_day)
    tianfu_branch = (4 - ziwei_branch) % 12

    placements: list[tuple[Star, int]] = []
    for star, offset in _ZIWEI_SERIES:
        placements.append((star, (ziwei_branch + offset) % 12))
    for star, offset in _TIANFU_SERIES:
        placements.append((star, (tianfu_branch + offset) % 12))

    stars_by_branch: list[list[Star]] = [[] for _ in range(12)]
    for star, branch in placements:
        stars_by_branch[branch].append(star)

    palace_branches = tuple((ming_branch - index) % 12 for index in range(12))
    palace_stems = tuple(_palace_stem(year_stem, branch) for branch in palace_branches)

    return ZiWeiChart(
        ming_branch=ming_branch,
        body_branch=body_branch,
        bureau=bureau,
        ziwei_branch=ziwei_branch,
        tianfu_branch=tianfu_branch,
        palace_branches=palace_branches,
        palace_stems=palace_stems,
        stars_by_branch=tuple(tuple(stars) for stars in stars_by_branch),
        year_stem=year_stem,
        year_branch=year_branch,
    )
