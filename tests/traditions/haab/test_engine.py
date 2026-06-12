from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.haab import (
    HAAB_DECK,
    HAAB_SPREAD,
    build_engine,
)


def test_cast_records_haab_and_summary() -> None:
    reading = build_engine().cast(_request("2012-12-21T00:00:00+00:00"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "haab"
    assert selection.symbol_id == "haab.month.kankin"
    assert selection.modifiers is not None
    assert selection.modifiers["haab"] == "3 K'ank'in"
    assert selection.modifiers["day"] == "3"
    assert reading.summary == "Haab' date 3 K'ank'in."


def test_wayeb_summary_flags_unlucky_days() -> None:
    reading = build_engine().cast(_request("2013-03-28T00:00:00+00:00"))

    assert reading.draw.selections[0].symbol_id == "haab.month.wayeb"
    assert reading.summary is not None
    assert "Wayeb'" in reading.summary


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("2012-12-21T00:00:00+00:00")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "anchor=2012-12-21-3-kankin" in reading.provenance.notes


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=HAAB_SPREAD.id, deck_id=HAAB_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "haab" not in fortune_telling_core.__all__


def _request(birth: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=HAAB_SPREAD.id,
        deck_id=HAAB_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": birth}),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )
