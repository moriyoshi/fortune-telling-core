from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
from fortune_telling_core.traditions.zi_wei.chart import BRANCH_CJK, compute_chart
from fortune_telling_core.traditions.zi_wei.periods import (
    active_da_xian,
    da_xian_ladder,
    liunian,
    nominal_age,
)

# Canonical reference chart, the same one ``test_chart.py`` validates against the
# 安命宮 month×hour table and the 納音 bureau: 1985 (乙丑) lunar month 3, day 15,
# hour 巳 → 命宮 亥, 土五局 (bureau 5).
_CHART = compute_chart(1985, 3, 15, 5)


def _branch(name: str) -> int:
    return BRANCH_CJK.index(name)


def test_reference_chart_anchors() -> None:
    assert BRANCH_CJK[_CHART.ming_branch] == "亥"
    assert _CHART.bureau == 5


def test_liunian_sits_on_the_taisui_branch_each_year() -> None:
    # 流年命宮 sits on the year's 太歲 branch — an externally fixed calendar fact.
    expected = {
        2023: ("癸卯", "卯"),
        2024: ("甲辰", "辰"),
        2025: ("乙巳", "巳"),
        2026: ("丙午", "午"),
    }
    for year, (ganzhi, branch) in expected.items():
        annual = liunian(_CHART, year)
        assert (annual.ganzhi_cjk, BRANCH_CJK[annual.palace.branch]) == (ganzhi, branch), year
    # 1984 is the cycle anchor 甲子 → 子 branch.
    assert BRANCH_CJK[liunian(_CHART, 1984).palace.branch] == "子"


def test_nominal_age_counts_from_one() -> None:
    assert nominal_age(1985, 1985) == 1
    assert nominal_age(1985, 2000) == 16


def test_da_xian_ladder_full_worked_example() -> None:
    # 土五局 → the 命宮 decade begins at 虚歳 5, each subsequent decade +10.
    # 順行 (陰年女) advances the branch 亥→子→丑→寅→卯→辰; 逆行 (陰年男) retreats
    # it 亥→戌→酉→申→未→午. The palace + resident stars come from the natal chart.
    female = da_xian_ladder(_CHART, LuckDirectionInput.FEMALE, count=6)
    male = da_xian_ladder(_CHART, LuckDirectionInput.MALE, count=6)

    assert [(d.start_age, d.end_age) for d in female] == [
        (5, 14),
        (15, 24),
        (25, 34),
        (35, 44),
        (45, 54),
        (55, 64),
    ]
    assert [BRANCH_CJK[d.palace.branch] for d in female] == ["亥", "子", "丑", "寅", "卯", "辰"]
    assert [BRANCH_CJK[d.palace.branch] for d in male] == ["亥", "戌", "酉", "申", "未", "午"]
    # Palace names and resident major stars for the 順行 ladder.
    assert [(d.palace.palace_cjk, d.palace.stars_cjk) for d in female] == [
        ("命宮", "天同"),
        ("父母宮", "武曲,天府"),
        ("福德宮", "太陽,太陰"),
        ("田宅宮", "貪狼"),
        ("官祿宮", "天機,巨門"),
        ("僕役宮", "紫微,天相"),
    ]


def test_active_da_xian_selects_the_decade_for_the_year() -> None:
    # 虚歳 16 in year 2000 → second decade (ages 15-24) for 土五局.
    decade = active_da_xian(_CHART, LuckDirectionInput.FEMALE, 1985, 2000)
    assert decade.index == 1
    assert (decade.start_age, decade.end_age) == (15, 24)
    assert BRANCH_CJK[decade.palace.branch] == "子"
    assert (decade.palace.palace_cjk, decade.palace.stars_cjk) == ("父母宮", "武曲,天府")
