from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.tzolkin import (
    TZOLKIN_DECK,
    TZOLKIN_SPREAD,
    build_engine,
)


def test_cast_records_day_sign_and_summary() -> None:
    reading = build_engine().cast(_request())

    selection = reading.draw.selections[0]
    assert selection.position_id == "day_sign"
    assert selection.symbol_id == "tzolkin.daysign.ajaw"
    assert selection.modifiers is not None
    assert selection.modifiers["tzolkin"] == "4 Ajaw"
    assert selection.modifiers["number"] == "4"
    assert reading.summary == "Tzolk'in day 4 Ajaw (Lord, south)."


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "correlation=gmt-584283" in reading.provenance.notes


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=TZOLKIN_SPREAD.id, deck_id=TZOLKIN_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "tzolkin" not in fortune_telling_core.__all__


def _request() -> ReadingRequest:
    return ReadingRequest(
        spread_id=TZOLKIN_SPREAD.id,
        deck_id=TZOLKIN_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": "2012-12-21T00:00:00+00:00"}),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )
