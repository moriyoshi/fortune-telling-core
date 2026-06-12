from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
from fortune_telling_core.traditions.four_pillars.luck import luck_forward
from fortune_telling_core.traditions.four_pillars.pillars import DAY_JIAZI_JDN
from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi, index_for
from fortune_telling_core.traditions.four_pillars.ten_gods import ten_god


def test_day_epoch_and_continuity() -> None:
    assert ganzhi(0).cjk == "甲子"
    assert (DAY_JIAZI_JDN + 1 - DAY_JIAZI_JDN) % 60 == 1


def test_five_tigers_and_five_rats_reference() -> None:
    # Jia year -> Bing Yin first month; Jia day -> Jia Zi first hour.
    assert index_for(2, 2) == 2
    assert index_for(0, 0) == 0


def test_ten_gods_table() -> None:
    assert ten_god(0, 0) == "friend"
    assert ten_god(0, 1) == "rob_wealth"
    assert ten_god(0, 2) == "eating_god"
    assert ten_god(0, 5) == "direct_wealth"
    assert ten_god(0, 6) == "seven_killings"
    assert ten_god(0, 9) == "direct_resource"


def test_luck_direction_combinations() -> None:
    assert luck_forward(0, LuckDirectionInput.MALE)
    assert not luck_forward(0, LuckDirectionInput.FEMALE)
    assert not luck_forward(1, LuckDirectionInput.MALE)
    assert luck_forward(1, LuckDirectionInput.FEMALE)
