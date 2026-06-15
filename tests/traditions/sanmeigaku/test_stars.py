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
