from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.sukuyo import (
    SUKUYO_DECK,
    SUKUYO_SPREAD,
    Ayanamsa,
    build_engine,
)
from fortune_telling_core.traditions.sukuyo.deck import SUKUYO_DECK as DECK
from fortune_telling_core.traditions.sukuyo.mansions import MANSIONS

_BIRTH = "1990-05-17T09:30:00+09:00"


def test_deck_has_27_unique_mansions() -> None:
    assert len(MANSIONS) == 27
    assert len({m.slug for m in MANSIONS}) == 27
    assert len({m.cjk for m in MANSIONS}) == 27
    assert len(DECK.symbols) == 27


def test_cast_records_birth_mansion() -> None:
    reading = build_engine().cast(_request())

    (selection,) = reading.draw.selections
    assert selection.position_id == "birth_mansion"
    assert selection.symbol_id == "sukuyo.mansion.shravana"
    assert selection.modifiers is not None
    assert selection.modifiers["cjk"] == "女宿"
    assert reading.summary is not None
    assert "女宿" in reading.summary


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert reading.provenance.rng_seed is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "ayanamsa=lahiri" in reading.provenance.notes
    assert "mansion_count=27" in reading.provenance.notes


def test_ayanamsa_changes_mansion() -> None:
    lahiri = build_engine().cast(_request())
    tropical = build_engine().cast(_request({"birth_datetime": _BIRTH, "ayanamsa": "none"}))

    assert lahiri.draw.selections[0].symbol_id != tropical.draw.selections[0].symbol_id
    assert "ayanamsa=none" in tropical.provenance.notes


def test_engine_default_ayanamsa_applies() -> None:
    reading = build_engine(ayanamsa=Ayanamsa.NONE).cast(_request())
    assert reading.draw.selections[0].symbol_id == "sukuyo.mansion.shatabhisha"


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=SUKUYO_SPREAD.id, deck_id=SUKUYO_DECK.id))


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SUKUYO_SPREAD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=SUKUYO_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "sukuyo" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=SUKUYO_SPREAD.id,
        deck_id=SUKUYO_DECK.id,
        querent=Querent("native", "Native", attrs or {"birth_datetime": _BIRTH}),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
    )
