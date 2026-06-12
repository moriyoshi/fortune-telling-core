import pytest

from fortune_telling_core import (
    ReadingRequest,
    SequenceRng,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.lenormand import (
    GRAND_TABLEAU,
    LENORMAND_DECK,
    SINGLE_CARD,
    THREE_CARD,
    build_engine,
)


def test_deck_has_36_numbered_cards() -> None:
    assert len(LENORMAND_DECK.symbols) == 36
    numbers = [int(symbol.attributes["number"]) for symbol in LENORMAND_DECK.symbols]
    assert numbers == list(range(1, 37))
    assert LENORMAND_DECK.symbols[0].name == "Rider"
    assert LENORMAND_DECK.symbols[-1].name == "Cross"


def test_read_then_replay_and_serde() -> None:
    request = ReadingRequest(spread_id=THREE_CARD.id, deck_id=LENORMAND_DECK.id)
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(ints=range(36)))

    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.positions == reading.positions
    assert reading_from_json(reading_to_json(reading)) == reading


def test_three_card_takes_first_three_in_order() -> None:
    request = ReadingRequest(spread_id=THREE_CARD.id, deck_id=LENORMAND_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(36)))

    assert [s.position_id for s in reading.draw.selections] == ["left", "center", "right"]
    assert reading.draw.selections[0].symbol_id == "lenormand.card.rider"


def test_grand_tableau_uses_all_36_cards_once() -> None:
    request = ReadingRequest(spread_id=GRAND_TABLEAU.id, deck_id=LENORMAND_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(36)))

    assert len(reading.draw.selections) == 36
    assert len({s.symbol_id for s in reading.draw.selections}) == 36


def test_no_orientation_modifiers() -> None:
    request = ReadingRequest(spread_id=SINGLE_CARD.id, deck_id=LENORMAND_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(36)))

    assert reading.draw.selections[0].modifiers in (None, {})


def test_unsupported_spread_and_deck() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=LENORMAND_DECK.id))
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SINGLE_CARD.id, deck_id="other"))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "lenormand" not in fortune_telling_core.__all__
