from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.celtic_tree import (
    CELTIC_TREE_DECK,
    CELTIC_TREE_SPREAD,
    build_engine,
)


def test_cast_records_sign_and_summary() -> None:
    reading = build_engine().cast(_request("1990-07-01T00:00:00+00:00"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "tree_sign"
    assert selection.symbol_id == "celtic_tree.sign.oak"
    assert selection.modifiers is not None
    assert selection.modifiers["ogham"] == "Duir"
    assert reading.summary == "Celtic tree sign Oak (Duir), Jun 10 – Jul 7."


def test_nameless_day_classifies_as_elder() -> None:
    reading = build_engine().cast(_request("1985-12-23T00:00:00+00:00"))

    assert reading.draw.selections[0].symbol_id == "celtic_tree.sign.elder"


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("1990-07-01T00:00:00+00:00")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "scheme=graves-white-goddess" in reading.provenance.notes


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=CELTIC_TREE_SPREAD.id, deck_id=CELTIC_TREE_DECK.id)
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "celtic_tree" not in fortune_telling_core.__all__


def _request(birth: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=CELTIC_TREE_SPREAD.id,
        deck_id=CELTIC_TREE_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": birth}),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )
