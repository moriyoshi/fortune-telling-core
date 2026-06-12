from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.tarot import RWS_DECK, THREE_CARD, build_engine


def test_same_seed_produces_identical_reading() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
    )
    engine = build_engine()

    assert engine.read(request, rng=RandomRng(77)) == engine.read(request, rng=RandomRng(77))


def test_different_seeds_differ() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
    )
    engine = build_engine()

    assert (
        engine.read(request, rng=RandomRng(77)).draw != engine.read(request, rng=RandomRng(78)).draw
    )
