from fortune_telling_core.traditions.sanmeigaku.stars import (
    MAIN_STARS,
    SUBORDINATE_STARS,
    life_stage_slug,
    main_star,
    subordinate_star,
)


def test_main_star_maps_ten_gods() -> None:
    # 甲 day stem (index 0) against 癸 (index 9): water generates wood across
    # polarities -> direct resource -> 玉堂星.
    assert main_star(0, 9).cjk == "玉堂星"
    # 甲 against 甲: same element, same polarity -> friend -> 貫索星.
    assert main_star(0, 0).cjk == "貫索星"
    assert set(MAIN_STARS) == {
        "friend",
        "rob_wealth",
        "eating_god",
        "hurting_officer",
        "indirect_wealth",
        "direct_wealth",
        "seven_killings",
        "direct_officer",
        "indirect_resource",
        "direct_resource",
    }


def test_life_stage_yang_and_yin_directions() -> None:
    # 甲 (yang) 長生 at 亥(11); 子(0) is the next stage 沐浴 -> 天恍星.
    assert life_stage_slug(0, 0) == "mokuyoku"
    assert subordinate_star(0, 0).cjk == "天恍星"
    # 乙 (yin) 長生 at 午(6) counted backwards -> 長生 itself -> 天貴星.
    assert life_stage_slug(1, 6) == "chosei"
    assert subordinate_star(1, 6).cjk == "天貴星"


def test_twelve_subordinate_stars_complete() -> None:
    assert len(SUBORDINATE_STARS) == 12
    # Every day stem visits all twelve stages across the twelve branches.
    for day_stem in range(10):
        stages = {life_stage_slug(day_stem, branch) for branch in range(12)}
        assert len(stages) == 12


def test_full_main_star_mapping_for_jia_day() -> None:
    # 通変星 -> 十大主星 for the 甲 day master against each of the ten stems.
    # 比肩貫索 劫財石門 食神鳳閣 傷官調舒 偏財禄存 正財司禄 偏官車騎 正官牽牛
    # 偏印龍高 印綬玉堂 — the standard (高尾) Sanmeigaku correspondence.
    expected = ["貫索星", "石門星", "鳳閣星", "調舒星", "禄存星",
                "司禄星", "車騎星", "牽牛星", "龍高星", "玉堂星"]
    assert [main_star(0, source).cjk for source in range(10)] == expected


def test_twelve_stage_long_life_anchors() -> None:
    # 長生 (Growth) branch for each day stem, from the standard 十二運 table —
    # independent of the implementation's own constant.
    chosei_branch = {
        0: 11,  # 甲 -> 亥
        1: 6,  # 乙 -> 午
        2: 2,  # 丙 -> 寅
        3: 9,  # 丁 -> 酉
        4: 2,  # 戊 -> 寅
        5: 9,  # 己 -> 酉
        6: 5,  # 庚 -> 巳
        7: 0,  # 辛 -> 子
        8: 8,  # 壬 -> 申
        9: 3,  # 癸 -> 卯
    }
    for stem, branch in chosei_branch.items():
        assert life_stage_slug(stem, branch) == "chosei"
        assert subordinate_star(stem, branch).cjk == "天貴星"
