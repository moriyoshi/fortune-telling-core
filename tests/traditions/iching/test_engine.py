import pytest

from fortune_telling_core import (
    ReadingRequest,
    SequenceRng,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.iching import (
    CASTING,
    ICHING_DECK,
    build_engine,
)

# Per coin, a float < 0.5 is heads (3), >= 0.5 is tails (2). Three coins/line.
_ALL_OLD_YANG = [0.0] * 18  # each line sums to 9 (old yang, changing)
_ALL_OLD_YIN = [0.9] * 18  # each line sums to 6 (old yin, changing)
_ALL_YOUNG_YANG = [0.9, 0.9, 0.0] * 6  # each line sums to 7 (young yang, stable)


def test_all_old_yang_casts_qian_changing_into_kun() -> None:
    reading = build_engine().read(_request(), rng=SequenceRng(floats=_ALL_OLD_YANG))

    primary, relating = reading.draw.selections
    assert primary.symbol_id == "iching.hexagram.1"  # Qian
    assert relating.symbol_id == "iching.hexagram.2"  # Kun
    assert primary.modifiers is not None
    assert primary.modifiers["changing_lines"] == "1,2,3,4,5,6"
    assert reading.summary is not None
    assert "Primary hexagram 1 Qian" in reading.summary
    assert "relating hexagram 2 Kun" in reading.summary


def test_all_old_yin_casts_kun_changing_into_qian() -> None:
    reading = build_engine().read(_request(), rng=SequenceRng(floats=_ALL_OLD_YIN))

    primary, relating = reading.draw.selections
    assert primary.symbol_id == "iching.hexagram.2"  # Kun
    assert relating.symbol_id == "iching.hexagram.1"  # Qian


def test_young_lines_have_no_changing_and_equal_relating() -> None:
    reading = build_engine().read(_request(), rng=SequenceRng(floats=_ALL_YOUNG_YANG))

    primary, relating = reading.draw.selections
    assert primary.symbol_id == "iching.hexagram.1"  # all young yang -> Qian
    assert relating.symbol_id == "iching.hexagram.1"  # unchanged
    assert primary.modifiers is not None
    assert primary.modifiers["changing_lines"] == ""
    assert reading.summary == "Primary hexagram 1 Qian; no changing lines."


def test_read_then_replay_and_serde() -> None:
    request = _request()
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(floats=_ALL_OLD_YANG))
    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=CASTING.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=ICHING_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "iching" not in fortune_telling_core.__all__


def _request() -> ReadingRequest:
    return ReadingRequest(spread_id=CASTING.id, deck_id=ICHING_DECK.id)
