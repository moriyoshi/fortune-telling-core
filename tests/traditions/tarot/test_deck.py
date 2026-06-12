from fortune_telling_core.traditions.tarot import RWS_DECK


def test_rws_deck_has_78_unique_cards() -> None:
    assert len(RWS_DECK.symbols) == 78
    assert len({symbol.id for symbol in RWS_DECK.symbols}) == 78


def test_rws_deck_attributes_are_well_formed() -> None:
    major = [symbol for symbol in RWS_DECK.symbols if symbol.attributes["arcana"] == "major"]
    minor = [symbol for symbol in RWS_DECK.symbols if symbol.attributes["arcana"] == "minor"]

    assert len(major) == 22
    assert len(minor) == 56
    assert all("number" in symbol.attributes for symbol in major)
    assert all({"suit", "rank"}.issubset(symbol.attributes) for symbol in minor)
