import pytest

from fortune_telling_core import (
    ReadingRequest,
    SequenceRng,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.geomancy import (
    GEOMANCY_DECK,
    SHIELD,
    build_engine,
)


def test_cast_fills_fifteen_shield_positions() -> None:
    request = ReadingRequest(spread_id=SHIELD.id, deck_id=GEOMANCY_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(floats=[0.0] * 16))

    assert len(reading.draw.selections) == 15
    assert reading.draw.selections[0].position_id == "mother_1"
    assert reading.draw.selections[-1].position_id == "judge"
    assert reading.draw.selections[-1].symbol_id == "geomancy.figure.populus"
    assert reading.summary is not None
    assert "Judge: Populus" in reading.summary


def test_read_then_replay_and_serde() -> None:
    request = ReadingRequest(spread_id=SHIELD.id, deck_id=GEOMANCY_DECK.id)
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(floats=[0.0, 0.9] * 8))
    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SHIELD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=GEOMANCY_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "geomancy" not in fortune_telling_core.__all__
