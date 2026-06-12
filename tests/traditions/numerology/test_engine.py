from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.numerology import (
    NUMEROLOGY_DECK,
    NUMEROLOGY_SPREAD,
    ReductionMethod,
    build_engine,
)


def test_cast_records_numbers_and_summary() -> None:
    reading = build_engine().cast(_request())

    assert tuple(s.position_id for s in reading.draw.selections) == ("life_path", "birthday")
    life_path, birthday = reading.draw.selections
    assert life_path.symbol_id == "numerology.number.5"
    assert birthday.symbol_id == "numerology.number.8"
    assert life_path.modifiers is not None
    assert life_path.modifiers["keyword"] == "Freedom"
    assert reading.summary == "Life Path 5 (Freedom); Birthday 8 (Power)."


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "reduction_method=component" in reading.provenance.notes


def test_request_reduction_method_override_changes_life_path() -> None:
    attrs = {"birth_datetime": "1985-09-01T00:00:00+00:00", "reduction_method": "iterative"}
    reading = build_engine().cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "numerology.number.33"
    assert reading.draw.selections[0].modifiers is not None
    assert reading.draw.selections[0].modifiers["master"] == "true"
    assert "reduction_method=iterative" in reading.provenance.notes


def test_engine_default_method_applies() -> None:
    attrs = {"birth_datetime": "1985-09-01T00:00:00+00:00"}
    reading = build_engine(reduction_method=ReductionMethod.ITERATIVE).cast(_request(attrs))

    assert reading.draw.selections[0].symbol_id == "numerology.number.33"


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=NUMEROLOGY_SPREAD.id, deck_id=NUMEROLOGY_DECK.id)
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "numerology" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=NUMEROLOGY_SPREAD.id,
        deck_id=NUMEROLOGY_DECK.id,
        querent=Querent(
            "native", "Native", attrs or {"birth_datetime": "1987-08-17T00:00:00+00:00"}
        ),
        requested_at=datetime(2026, 6, 13, tzinfo=UTC),
    )
