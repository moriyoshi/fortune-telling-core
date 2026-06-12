from fortune_telling_core import ReadingRequest, SequenceRng
from fortune_telling_core.traditions.tarot import RWS_DECK, THREE_CARD, build_engine


def test_allow_reversals_toggles_orientation_deterministically() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
        options={"allow_reversals": "true"},
    )
    reading = build_engine().read(
        request,
        rng=SequenceRng(ints=range(78), floats=[0.1, 0.5, 0.9]),
    )

    assert [selection.modifiers for selection in reading.draw.selections] == [
        {"orientation": "reversed"},
        {"orientation": "upright"},
        {"orientation": "upright"},
    ]


def test_reversals_disabled_has_no_orientation_modifier() -> None:
    request = ReadingRequest(
        spread_id=THREE_CARD.id,
        deck_id=RWS_DECK.id,
    )
    reading = build_engine().read(request, rng=SequenceRng(ints=range(78)))

    assert [selection.modifiers for selection in reading.draw.selections] == [{}, {}, {}]
