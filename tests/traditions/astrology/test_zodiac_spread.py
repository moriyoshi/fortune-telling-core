from fortune_telling_core.traditions.astrology import NATAL_CHART, SIDEREAL_ZODIAC, TROPICAL_ZODIAC


def test_zodiac_decks_have_12_unique_signs() -> None:
    assert len(TROPICAL_ZODIAC.symbols) == 12
    assert len(SIDEREAL_ZODIAC.symbols) == 12
    assert {symbol.id for symbol in TROPICAL_ZODIAC.symbols} == {
        symbol.id for symbol in SIDEREAL_ZODIAC.symbols
    }


def test_natal_spread_has_body_and_angle_positions() -> None:
    assert NATAL_CHART.size == 14
    assert NATAL_CHART.positions[0].id == "sun"
    assert NATAL_CHART.positions[-2].id == "ascendant"
    assert NATAL_CHART.positions[-1].id == "midheaven"
