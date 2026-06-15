from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi, index_for
from fortune_telling_core.traditions.koyomi.calendar_notes import (
    ROKUYO,
    is_ichiryu_manbai,
    is_sanrinbo,
    is_tensha,
    rokuyo_index,
)


def _ganzhi(stem: int, branch: int):  # type: ignore[no-untyped-def]
    return ganzhi(index_for(stem, branch))


def test_rokuyo_mapping_and_anchor() -> None:
    assert [slug for slug, _, _ in ROKUYO] == [
        "taian",
        "shakko",
        "sensho",
        "tomobiki",
        "sembu",
        "butsumetsu",
    ]
    # 旧暦 1/1 -> (1+1)%6 = 2 -> 先勝.
    assert rokuyo_index(1, 1) == 2
    assert ROKUYO[rokuyo_index(1, 1)][1] == "先勝"


def test_tensha_is_seasonal_ganzhi() -> None:
    # Spring (節月 0-2) 戊寅; summer (3-5) 甲午; autumn (6-8) 戊申; winter (9-11) 甲子.
    wu_yin = _ganzhi(4, 2)  # 戊寅
    jia_wu = _ganzhi(0, 6)  # 甲午
    assert is_tensha(0, wu_yin) is True  # 正月 (spring) + 戊寅
    assert is_tensha(2, wu_yin) is True  # 三月 still spring
    assert is_tensha(0, jia_wu) is False  # wrong 干支 for spring
    assert is_tensha(3, jia_wu) is True  # 四月 (summer) + 甲午
    assert is_tensha(9, _ganzhi(0, 0)) is True  # 十月 (winter) + 甲子


def test_ichiryu_manbai_uses_sectional_month_branches() -> None:
    # 正月 (index 0): 丑(1) and 午(6) are 一粒万倍日; others are not.
    assert is_ichiryu_manbai(0, 1) is True
    assert is_ichiryu_manbai(0, 6) is True
    assert is_ichiryu_manbai(0, 0) is False


def test_sanrinbo_branch_by_month_group() -> None:
    # 節月 groups: {正四七十}->亥(11), {二五八十一}->寅(2), {三六九十二}->午(6).
    assert is_sanrinbo(0, 11) is True  # 正月 -> 亥
    assert is_sanrinbo(3, 11) is True  # 四月 -> 亥 (same group)
    assert is_sanrinbo(1, 2) is True  # 二月 -> 寅
    assert is_sanrinbo(2, 6) is True  # 三月 -> 午
    assert is_sanrinbo(0, 6) is False  # 正月 is not 午
