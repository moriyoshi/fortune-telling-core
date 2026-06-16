"""Zi Wei time-varying periods: 大限 (decade limits) and 流年 (annual).

Both relocate the 命宮 pointer over a natal chart; neither moves the fourteen
major stars (the moving 流 stars and 四化 are minor/divergent and out of scope,
like the natal minor stars).

* 流年 (annual) — the 流年命宮 sits on the palace whose earthly branch equals
  the target year's branch (the 太歲 branch). Direction-independent.
* 大限 (decade limits) — each palace governs ten years. The first 大限 is the
  命宮, beginning at the 五行局 number in 虚歳 (數え年, born = age 1): 水二局 → 2,
  木三局 → 3, …, 火六局 → 6. Successive decades step through the palaces 順行 for
  陽年男 / 陰年女 and 逆行 for 陰年男 / 陽年女 — the same polarity × gender rule as
  :func:`fortune_telling_core.traditions.four_pillars.luck.luck_forward`, where
  順行 advances the earthly branch (命宮 → 父母宮 → …) and 逆行 retreats it
  (命宮 → 兄弟宮 → …).
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
from fortune_telling_core.traditions.four_pillars.luck import luck_forward
from fortune_telling_core.traditions.four_pillars.sexagenary import annual_index, ganzhi
from fortune_telling_core.traditions.zi_wei.chart import PALACES, Star, ZiWeiChart


@dataclass(frozen=True, slots=True)
class PalacePeriod:
    """A palace identified as the focus of a period, with its resident stars."""

    branch: int
    palace_slug: str
    palace_cjk: str
    stars: tuple[Star, ...]

    @property
    def stars_cjk(self) -> str:
        return ",".join(star.cjk for star in self.stars)


@dataclass(frozen=True, slots=True)
class Liunian:
    """流年: the annual 命宮 for a target year."""

    year: int
    ganzhi_cjk: str
    palace: PalacePeriod


@dataclass(frozen=True, slots=True)
class DaXian:
    """大限: a ten-year decade limit."""

    index: int  # 0-based decade (0 = the 命宮 decade)
    start_age: int  # 虚歳 (數え年)
    end_age: int
    forward: bool
    palace: PalacePeriod


def _palace_on_branch(chart: ZiWeiChart, branch: int) -> PalacePeriod:
    index = (chart.ming_branch - branch) % 12
    slug, cjk = PALACES[index]
    return PalacePeriod(branch, slug, cjk, chart.stars_by_branch[branch])


def liunian(chart: ZiWeiChart, year: int) -> Liunian:
    """Return the 流年命宮 for ``year``."""

    gz = annual_index(year)
    return Liunian(year=year, ganzhi_cjk=ganzhi(gz).cjk, palace=_palace_on_branch(chart, gz % 12))


def da_xian_forward(chart: ZiWeiChart, gender: LuckDirectionInput) -> bool:
    """Return whether 大限 advances the earthly branch (順行)."""

    return luck_forward(chart.year_stem, gender)


def nominal_age(birth_lunar_year: int, year: int) -> int:
    """虚歳 (數え年) in ``year`` for someone born in ``birth_lunar_year``."""

    return year - birth_lunar_year + 1


def da_xian_ladder(
    chart: ZiWeiChart, gender: LuckDirectionInput, *, count: int = 12
) -> tuple[DaXian, ...]:
    """Return the first ``count`` 大限 decades from the 命宮."""

    forward = da_xian_forward(chart, gender)
    ladder: list[DaXian] = []
    for index in range(count):
        step = index if forward else -index
        branch = (chart.ming_branch + step) % 12
        start = chart.bureau + 10 * index
        ladder.append(
            DaXian(
                index=index,
                start_age=start,
                end_age=start + 9,
                forward=forward,
                palace=_palace_on_branch(chart, branch),
            )
        )
    return tuple(ladder)


def active_da_xian(
    chart: ZiWeiChart, gender: LuckDirectionInput, birth_lunar_year: int, year: int
) -> DaXian:
    """Return the 大限 decade in force during ``year``.

    Ages before the first decade (虚歳 < 五行局) clamp to the 命宮 decade.
    """

    forward = da_xian_forward(chart, gender)
    age = nominal_age(birth_lunar_year, year)
    index = max(0, (age - chart.bureau) // 10)
    step = index if forward else -index
    branch = (chart.ming_branch + step) % 12
    start = chart.bureau + 10 * index
    return DaXian(
        index=index,
        start_age=start,
        end_age=start + 9,
        forward=forward,
        palace=_palace_on_branch(chart, branch),
    )
