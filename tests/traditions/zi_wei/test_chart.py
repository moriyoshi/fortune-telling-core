from fortune_telling_core.traditions.zi_wei.chart import (
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
