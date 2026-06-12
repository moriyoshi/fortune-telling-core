from fortune_telling_core import ReadingRequest, SequenceRng
from fortune_telling_core.traditions.tarot import RWS_DECK, THREE_CARD, build_engine


def test_read_then_replay_draw_produces_same_positions() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
    )
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(ints=range(78)))

    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.positions == reading.positions
    assert replayed.provenance.rng_kind is None


def test_sequence_rng_forces_exact_draw() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
    )
    reading = build_engine().read(request, rng=SequenceRng(ints=range(77, -1, -1)))

    assert [selection.symbol_id for selection in reading.draw.selections] == [
        RWS_DECK.symbols[77].id,
        RWS_DECK.symbols[76].id,
        RWS_DECK.symbols[75].id,
    ]
