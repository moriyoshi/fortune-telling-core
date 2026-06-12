from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.weton import (
    WETON_DECK,
    WETON_SPREAD,
    DayBoundary,
    build_engine,
)


def test_cast_records_expected_positions_and_modifiers() -> None:
    reading = build_engine().cast(_request())

    assert tuple(selection.position_id for selection in reading.draw.selections) == (
        "saptawara",
        "pancawara",
    )
    saptawara, pancawara = reading.draw.selections
    assert saptawara.symbol_id == "weton.saptawara.jumat"
    assert pancawara.symbol_id == "weton.pancawara.legi"
    assert saptawara.modifiers is not None
    assert saptawara.modifiers["weton"] == "Jumat Legi"
    assert saptawara.modifiers["neptu"] == "11"
    assert reading.summary == "Weton Jumat Legi: neptu 6 + 5 = 11."


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "pancawara_anchor=1945-08-17-jumat-legi" in reading.provenance.notes
    assert "day_boundary=midnight" in reading.provenance.notes


def test_request_day_boundary_override_changes_weton_and_provenance() -> None:
    attrs = {"birth_datetime": "1945-08-17T19:00:00+07:00", "day_boundary": "sunset"}
    reading = build_engine().cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "weton.saptawara.sabtu"
    assert reading.draw.selections[1].symbol_id == "weton.pancawara.pahing"
    assert "day_boundary=sunset" in reading.provenance.notes


def test_engine_default_day_boundary_applies() -> None:
    attrs = {"birth_datetime": "1945-08-17T19:00:00+07:00"}
    reading = build_engine(day_boundary=DayBoundary.SUNSET).cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "weton.saptawara.sabtu"


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=WETON_SPREAD.id, deck_id=WETON_DECK.id))


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=WETON_SPREAD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=WETON_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "weton" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=WETON_SPREAD.id,
        deck_id=WETON_DECK.id,
        querent=Querent("native", "Native", attrs or _attrs()),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )


def _attrs() -> dict[str, str]:
    return {"birth_datetime": "1945-08-17T10:00:00+07:00"}
