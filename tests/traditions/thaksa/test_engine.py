from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.thaksa import (
    THAKSA_DECK,
    THAKSA_SPREAD,
    build_engine,
)


def test_cast_records_houses_and_summary() -> None:
    reading = build_engine().cast(_request())

    assert tuple(s.position_id for s in reading.draw.selections) == (
        "boriwan",
        "ayu",
        "det",
        "si",
        "mula",
        "utsaha",
        "montri",
        "kalakini",
    )
    boriwan = reading.draw.selections[0]
    assert boriwan.symbol_id == "thaksa.graha.athit"
    assert boriwan.modifiers is not None
    assert boriwan.modifiers["ruler"] == "Sun"
    assert boriwan.modifiers["kalakini"] == "Venus"
    assert reading.summary is not None
    assert "Ruling graha Sun" in reading.summary
    assert "Kalakini: Venus" in reading.summary


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_wednesday_night_summary_flags_night() -> None:
    attrs = {"birth_datetime": "2000-01-05T20:00:00+07:00"}
    reading = build_engine().cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "thaksa.graha.rahu"
    assert reading.summary is not None
    assert "Rahu (night)" in reading.summary


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=THAKSA_SPREAD.id, deck_id=THAKSA_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "thaksa" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=THAKSA_SPREAD.id,
        deck_id=THAKSA_DECK.id,
        querent=Querent("native", "Native", attrs or _attrs()),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )


def _attrs() -> dict[str, str]:
    return {"birth_datetime": "1990-04-15T09:00:00+07:00"}  # a Sunday
