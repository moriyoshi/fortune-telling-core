"""Sanmeigaku star tables.

Two star families are derived from the Four Pillars stems and branches:

* 十大主星 (ten main stars) — the Sanmeigaku naming of the Four Pillars
  通変星 (Ten Gods). Each main star is the relationship between the day stem
  (日干) and a source stem, so it reuses
  :func:`fortune_telling_core.traditions.four_pillars.ten_gods.ten_god`.
* 十二大従星 (twelve subordinate stars) — the Sanmeigaku naming of the
  十二運 (twelve life-cycle stages). Each subordinate star is the life-cycle
  stage of the day stem against an earthly branch.

The 主星 ↔ 通変星 and 従星 ↔ 十二運 correspondences are the standard ones used
by mainstream (高尾) Sanmeigaku.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.stems_branches import stem
from fortune_telling_core.traditions.four_pillars.ten_gods import ten_god


@dataclass(frozen=True, slots=True)
class Star:
    """A Sanmeigaku star (main or subordinate)."""

    slug: str
    cjk: str
    name: str


# 十大主星 keyed by the Four Pillars Ten-God label returned by ``ten_god``.
MAIN_STARS: dict[str, Star] = {
    "friend": Star("kansaku", "貫索星", "Kansaku"),
    "rob_wealth": Star("sekimon", "石門星", "Sekimon"),
    "eating_god": Star("hokaku", "鳳閣星", "Hokaku"),
    "hurting_officer": Star("chosho", "調舒星", "Chosho"),
    "indirect_wealth": Star("rokuson", "禄存星", "Rokuson"),
    "direct_wealth": Star("shiroku", "司禄星", "Shiroku"),
    "seven_killings": Star("shaki", "車騎星", "Shaki"),
    "direct_officer": Star("kengyu", "牽牛星", "Kengyu"),
    "indirect_resource": Star("ryuko", "龍高星", "Ryuko"),
    "direct_resource": Star("gyokudo", "玉堂星", "Gyokudo"),
}

# 十二運 stages in cycle order starting at 長生 (Growth).
_STAGES: tuple[str, ...] = (
    "chosei",  # 長生
    "mokuyoku",  # 沐浴
    "kantai",  # 冠帯
    "kenroku",  # 建禄 (臨官)
    "teio",  # 帝旺
    "sui",  # 衰
    "byo",  # 病
    "shi",  # 死
    "bo",  # 墓
    "zetsu",  # 絶
    "tai",  # 胎
    "yo",  # 養
)

# 十二大従星 keyed by 十二運 stage slug.
SUBORDINATE_STARS: dict[str, Star] = {
    "chosei": Star("tenki", "天貴星", "Tenki"),
    "mokuyoku": Star("tenkou", "天恍星", "Tenkou"),
    "kantai": Star("tennan", "天南星", "Tennan"),
    "kenroku": Star("tenroku", "天禄星", "Tenroku"),
    "teio": Star("tensho", "天将星", "Tensho"),
    "sui": Star("tendo", "天堂星", "Tendo"),
    "byo": Star("tenko", "天胡星", "Tenko"),
    "shi": Star("tenkyoku", "天極星", "Tenkyoku"),
    "bo": Star("tenkura", "天庫星", "Tenkura"),
    "zetsu": Star("tenso", "天馳星", "Tenso"),
    "tai": Star("tenpo", "天報星", "Tenpo"),
    "yo": Star("tenin", "天印星", "Tenin"),
}

# Earthly branch (index) holding 長生 for each heavenly stem (index).
# Yang stems advance forward through the branches; yin stems retreat.
_CHOSEI_BRANCH: tuple[int, ...] = (
    11,  # 甲 -> 亥
    6,  # 乙 -> 午
    2,  # 丙 -> 寅
    9,  # 丁 -> 酉
    2,  # 戊 -> 寅
    9,  # 己 -> 酉
    5,  # 庚 -> 巳
    0,  # 辛 -> 子
    8,  # 壬 -> 申
    3,  # 癸 -> 卯
)

ALL_STARS: tuple[Star, ...] = tuple(MAIN_STARS.values()) + tuple(SUBORDINATE_STARS.values())


def main_star(day_stem_index: int, source_stem_index: int) -> Star:
    """Return the 主星 of a source stem relative to the day stem."""

    return MAIN_STARS[ten_god(day_stem_index, source_stem_index)]


def life_stage_index(day_stem_index: int, branch_index: int) -> int:
    """Return the 十二運 stage index (0=長生 … 11=養) for a day stem at a branch."""

    chosei = _CHOSEI_BRANCH[day_stem_index % 10]
    forward = stem(day_stem_index).polarity.value == "yang"
    if forward:
        return (branch_index - chosei) % 12
    return (chosei - branch_index) % 12


def life_stage_slug(day_stem_index: int, branch_index: int) -> str:
    """Return the 十二運 stage slug for a day stem at a branch."""

    return _STAGES[life_stage_index(day_stem_index, branch_index)]


def subordinate_star(day_stem_index: int, branch_index: int) -> Star:
    """Return the 従星 of a branch relative to the day stem."""

    return SUBORDINATE_STARS[life_stage_slug(day_stem_index, branch_index)]
