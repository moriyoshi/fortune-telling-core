from fortune_telling_core.traditions.four_pillars import FOUR_PILLARS_DECK, FOUR_PILLARS_SPREAD
from fortune_telling_core.traditions.four_pillars.sexagenary import annual_index, ganzhi
from fortune_telling_core.traditions.four_pillars.stems_branches import BRANCHES


def test_deck_and_spread_shape() -> None:
    assert len(FOUR_PILLARS_DECK.symbols) == 22
    assert FOUR_PILLARS_SPREAD.size == 8
    assert FOUR_PILLARS_SPREAD.positions[0].id == "year_stem"


def test_hidden_stems_are_pinned() -> None:
    assert BRANCHES[1].hidden_stems == (5, 9, 7)
    assert BRANCHES[2].hidden_stems == (0, 2, 4)
    assert BRANCHES[11].hidden_stems == (8, 0)


def test_annual_pillar_reference_years() -> None:
    assert annual_index(1984) == 0
    assert ganzhi(annual_index(1984)).cjk == "甲子"
    assert ganzhi(annual_index(2024)).cjk == "甲辰"
