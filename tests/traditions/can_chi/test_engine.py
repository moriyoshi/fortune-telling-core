from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.can_chi import (
    CAN_CHI_DECK,
    CAN_CHI_SPREAD,
    DayBoundary,
    build_engine,
)


def test_cast_records_pillars_and_summary() -> None:
    reading = build_engine().cast(_request())

    assert tuple(s.position_id for s in reading.draw.selections) == (
        "day_can",
        "day_chi",
        "hour_can",
        "hour_chi",
    )
    day_can, day_chi = reading.draw.selections[0], reading.draw.selections[1]
    assert day_can.symbol_id == "cc.can.binh"
    assert day_chi.symbol_id == "cc.chi.dan"
    assert day_chi.modifiers is not None
    assert day_chi.modifiers["animal"] == "Tiger"
    assert day_chi.modifiers["day_pillar"] == "Bính Dần"
    assert reading.summary is not None
    assert "Day pillar Bính Dần (Tiger)" in reading.summary


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "day_anchor=2000-01-07-giap-ty" in reading.provenance.notes
    assert "day_boundary=midnight" in reading.provenance.notes


def test_request_day_boundary_override_changes_day_and_provenance() -> None:
    attrs = {"birth_datetime": "1984-02-02T23:30:00+07:00", "day_boundary": "late_ty"}
    reading = build_engine().cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "cc.can.dinh"  # Đinh (next day)
    assert reading.draw.selections[1].symbol_id == "cc.chi.mao"  # Mão
    assert "day_boundary=late_ty" in reading.provenance.notes


def test_engine_default_day_boundary_applies() -> None:
    attrs = {"birth_datetime": "1984-02-02T23:30:00+07:00"}
    reading = build_engine(day_boundary=DayBoundary.LATE_TY).cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "cc.can.dinh"


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=CAN_CHI_SPREAD.id, deck_id=CAN_CHI_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "can_chi" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=CAN_CHI_SPREAD.id,
        deck_id=CAN_CHI_DECK.id,
        querent=Querent("native", "Native", attrs or _attrs()),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )


def _attrs() -> dict[str, str]:
    return {"birth_datetime": "1984-02-02T12:00:00+07:00"}  # Bính Dần day
