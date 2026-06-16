from fortune_telling_core.traditions.sanmeigaku.periods import annual_stars, daiun_columns

# Worked examples for a 丙 (index 2) day master. The year 干支 are externally
# fixed calendar facts; the 主星 / 従星 follow the canonical (高尾) 通変星 →
# 十大主星 and 十二運 → 十二大従星 tables that ``test_stars.py`` anchors.
#
# 2023 癸卯: 癸→正官→牽牛星; 丙 沐浴 at 卯→天恍星.
# 2024 甲辰: 甲→偏印→龍高星; 丙 冠帯 at 辰→天南星.
# 2025 乙巳: 乙→正印→玉堂星; 丙 建禄 at 巳→天禄星.
# 2026 丙午: 丙→比肩→貫索星; 丙 帝旺 at 午→天将星.
_ANNUAL = {
    2023: ("癸卯", "牽牛星", "天恍星"),
    2024: ("甲辰", "龍高星", "天南星"),
    2025: ("乙巳", "玉堂星", "天禄星"),
    2026: ("丙午", "貫索星", "天将星"),
}


def test_annual_stars_match_worked_examples() -> None:
    for year, (ganzhi, main, subordinate) in _ANNUAL.items():
        stars = annual_stars(2, year)
        assert (stars.ganzhi.cjk, stars.main.cjk, stars.subordinate.cjk) == (
            ganzhi,
            main,
            subordinate,
        ), year
    # 1984 is the sexagenary cycle anchor 甲子.
    assert annual_stars(2, 1984).ganzhi.cjk == "甲子"


def test_daiun_ganzhi_ladder_is_sequential_in_both_directions() -> None:
    # From the 乙丑 month pillar (cycle index 1), 順行 walks the sexagenary cycle
    # forward and 逆行 backward — pure calendar arithmetic, independent of the
    # day master.
    forward = daiun_columns(2, 1, forward=True, start_age=1.0, count=6)
    backward = daiun_columns(2, 1, forward=False, start_age=9.0, count=6)
    assert [c.stars.cjk for c in forward] == ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未"]
    assert [c.stars.cjk for c in backward] == ["甲子", "癸亥", "壬戌", "辛酉", "庚申", "己未"]
    # Each column carries the 主星 / 従星 of its 干支 for the 丙 day master.
    assert [(c.stars.main.cjk, c.stars.subordinate.cjk) for c in forward] == [
        ("貫索星", "天貴星"),  # 丙寅
        ("石門星", "天恍星"),  # 丁卯
        ("鳳閣星", "天南星"),  # 戊辰
        ("調舒星", "天禄星"),  # 己巳
        ("禄存星", "天将星"),  # 庚午
        ("司禄星", "天堂星"),  # 辛未
    ]


def test_daiun_columns_step_ten_years_from_the_start_age() -> None:
    columns = daiun_columns(2, 1, forward=True, start_age=2.0, count=4)
    assert [c.start_age for c in columns] == [2.0, 12.0, 22.0, 32.0]
    assert [c.index for c in columns] == [0, 1, 2, 3]
