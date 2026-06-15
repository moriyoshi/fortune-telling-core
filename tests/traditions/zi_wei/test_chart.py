from fortune_telling_core.traditions.four_pillars.sexagenary import index_for
from fortune_telling_core.traditions.zi_wei.chart import (
    _NAYIN_BUREAU,
    BRANCH_CJK,
    MAJOR_STARS,
    _ziwei_branch,
    compute_chart,
)


def _branch(name: str) -> int:
    return BRANCH_CJK.index(name)


def test_qi_ziwei_matches_canonical_water_bureau() -> None:
    # 水二局: 初一丑、初二寅、初三寅、初四卯、初五卯、初六辰、初七辰、初八巳。
    expected = {1: "丑", 2: "寅", 3: "寅", 4: "卯", 5: "卯", 6: "辰", 7: "辰", 8: "巳"}
    for day, branch in expected.items():
        assert BRANCH_CJK[_ziwei_branch(2, day)] == branch


def test_qi_ziwei_matches_canonical_fire_bureau() -> None:
    # 火六局: 初一酉、初二午、初三亥、初四辰、初五丑、初六寅、初七戌、初八未、初九子。
    expected = {1: "酉", 2: "午", 3: "亥", 4: "辰", 5: "丑", 6: "寅", 7: "戌", 8: "未", 9: "子"}
    for day, branch in expected.items():
        assert BRANCH_CJK[_ziwei_branch(6, day)] == branch


def test_tianfu_is_reflection_of_ziwei() -> None:
    for day in range(1, 31):
        chart = compute_chart(1985, 3, day, 0)
        assert chart.tianfu_branch == (4 - chart.ziwei_branch) % 12


def test_fourteen_majors_and_structural_opposites() -> None:
    chart = compute_chart(1985, 3, 15, 5)
    placement = {star.slug: b for b in range(12) for star in chart.stars_by_branch[b]}
    assert len(placement) == len(MAJOR_STARS) == 14
    # 七殺 always opposite 天府; 破軍 always opposite 天相.
    assert (placement["qisha"] - placement["tianfu"]) % 12 == 6
    assert (placement["pojun"] - placement["tianxiang"]) % 12 == 6


def test_life_palace_and_bureau_reference_chart() -> None:
    # 1985 (乙丑), lunar month 3, day 15, hour 巳: 命宮 丁亥 -> 土五局.
    chart = compute_chart(1985, 3, 15, 5)
    assert chart.ming_branch == _branch("亥")
    assert chart.bureau == 5
    assert chart.ziwei_branch == _branch("辰")


def test_bureau_matches_known_nayin_elements() -> None:
    # 五行局 = 納音 element of the 命宮 stem-branch (水2 木3 金4 土5 火6).
    # Known 納音: 甲子海中金, 丙寅爐中火, 戊辰大林木, 庚午路旁土, 壬戌大海水.
    stem = {"甲": 0, "丙": 2, "戊": 4, "庚": 6, "壬": 8}
    branch = {"子": 0, "寅": 2, "辰": 4, "午": 6, "戌": 10}
    cases = {("甲", "子"): 4, ("丙", "寅"): 6, ("戊", "辰"): 3, ("庚", "午"): 5, ("壬", "戌"): 2}
    for (gan, zhi), bureau in cases.items():
        pair = index_for(stem[gan], branch[zhi]) // 2
        assert _NAYIN_BUREAU[pair] == bureau


def test_life_palace_matches_canonical_month_hour_table() -> None:
    # 命宮 from the canonical 安命宮 month x hour table (寅 starts month 1).
    # month 1 / hour 子 -> 寅; month 1 / hour 亥 -> 卯; month 3 / hour 午 -> 戌.
    assert compute_chart(2000, 1, 1, 0).ming_branch == _branch("寅")
    assert compute_chart(2000, 1, 1, 11).ming_branch == _branch("卯")
    assert compute_chart(2000, 3, 1, 6).ming_branch == _branch("戌")
