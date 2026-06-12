import pytest

from fortune_telling_core import (
    ReadingRequest,
    SequenceRng,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.runes import (
    NORNS,
    RUNE_DECK,
    SINGLE_RUNE,
    build_engine,
)
from fortune_telling_core.traditions.runes.runes import RUNES


def _permutation_first(index: int) -> list[int]:
    return [index, *[i for i in range(len(RUNES)) if i != index]]


def test_deck_has_24_runes_with_eight_non_reversible() -> None:
    assert len(RUNE_DECK.symbols) == 24
    assert sum(1 for rune in RUNES if not rune.reversible) == 8
    # The symmetrical runes that have no merkstave form.
    non_reversible = {rune.slug for rune in RUNES if not rune.reversible}
    assert non_reversible == {
        "gebo",
        "hagalaz",
        "isa",
        "jera",
        "eihwaz",
        "sowilo",
        "ingwaz",
        "dagaz",
    }


def test_read_then_replay_produces_same_positions() -> None:
    request = ReadingRequest(spread_id=NORNS.id, deck_id=RUNE_DECK.id)
    engine = build_engine()
    reading = engine.read(request, rng=SequenceRng(ints=range(24)))

    replayed = engine.replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.positions == reading.positions
    assert reading_from_json(reading_to_json(reading)) == reading


def test_reversible_rune_can_be_reversed() -> None:
    # Fehu (index 0) is reversible; float 0.0 < 0.5 turns it.
    request = ReadingRequest(
        spread_id=SINGLE_RUNE.id, deck_id=RUNE_DECK.id, options={"allow_reversals": "true"}
    )
    reading = build_engine().read(
        request, rng=SequenceRng(ints=_permutation_first(0), floats=[0.0])
    )

    selection = reading.draw.selections[0]
    assert selection.symbol_id == "runes.rune.fehu"
    assert selection.modifiers == {"orientation": "reversed"}


def test_symmetrical_rune_is_never_reversed() -> None:
    # Isa (index 10) is symmetrical; even with float 0.0 it stays upright.
    request = ReadingRequest(
        spread_id=SINGLE_RUNE.id, deck_id=RUNE_DECK.id, options={"allow_reversals": "true"}
    )
    reading = build_engine().read(
        request, rng=SequenceRng(ints=_permutation_first(10), floats=[0.0])
    )

    selection = reading.draw.selections[0]
    assert selection.symbol_id == "runes.rune.isa"
    assert selection.modifiers == {"orientation": "upright"}


def test_no_orientation_without_reversals() -> None:
    request = ReadingRequest(spread_id=SINGLE_RUNE.id, deck_id=RUNE_DECK.id)
    reading = build_engine().read(request, rng=SequenceRng(ints=range(24)))

    assert reading.draw.selections[0].modifiers == {}


def test_unsupported_spread_and_deck() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=RUNE_DECK.id))
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SINGLE_RUNE.id, deck_id="other"))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "runes" not in fortune_telling_core.__all__
