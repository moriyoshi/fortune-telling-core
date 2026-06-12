import pytest

from fortune_telling_core import (
    ReadingRequest,
    SequenceRng,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.dominoes import (
    DOMINOES_DECK,
    SINGLE_TILE,
    THREE_TILES,
    build_engine,
)
from fortune_telling_core.traditions.dominoes.tiles import TILES


def test_double_six_set_has_28_tiles_with_7_doubles() -> None:
    assert len(TILES) == 28
    assert len(DOMINOES_DECK.symbols) == 28
    assert sum(1 for tile in TILES if tile.double) == 7
    assert all(tile.high >= tile.low for tile in TILES)
    assert len({tile.symbol_id for tile in TILES}) == 28


def test_first_and_last_tiles() -> None:
    assert DOMINOES_DECK.symbols[0].id == "dominoes.tile.0_0"
    assert DOMINOES_DECK.symbols[-1].id == "dominoes.tile.6_6"
    assert DOMINOES_DECK.symbols[-1].attributes["pips"] == "12"


def test_read_then_replay_and_serde() -> None:
    request = ReadingRequest(spread_id=THREE_TILES.id, deck_id=DOMINOES_DECK.id)
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(ints=range(28)))

    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.positions == reading.positions
    assert reading_from_json(reading_to_json(reading)) == reading


def test_three_tiles_positions_and_order() -> None:
    request = ReadingRequest(spread_id=THREE_TILES.id, deck_id=DOMINOES_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(28)))

    assert [s.position_id for s in reading.draw.selections] == ["past", "present", "future"]
    assert reading.draw.selections[0].symbol_id == "dominoes.tile.0_0"


def test_single_tile_has_no_modifiers() -> None:
    request = ReadingRequest(spread_id=SINGLE_TILE.id, deck_id=DOMINOES_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(28)))

    assert reading.draw.selections[0].modifiers in (None, {})


def test_unsupported_spread_and_deck() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=DOMINOES_DECK.id))
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SINGLE_TILE.id, deck_id="other"))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "dominoes" not in fortune_telling_core.__all__
