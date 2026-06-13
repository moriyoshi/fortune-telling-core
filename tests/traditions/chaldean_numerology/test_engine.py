import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.chaldean_numerology import (
    CHALDEAN_NUMEROLOGY_DECK,
    CHALDEAN_NUMEROLOGY_SPREAD,
    build_engine,
)


def test_cast_records_name_number_and_summary() -> None:
    reading = build_engine().cast(_request("John"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "name_number"
    assert selection.symbol_id == "chaldean_numerology.number.9"
    assert selection.modifiers is not None
    assert selection.modifiers["planet"] == "Mars"
    assert selection.modifiers["total"] == "18"
    assert selection.modifiers["value_system"] == "latin_chaldean.v1"
    assert selection.modifiers["normalization"] == "latin_ascii_ignore"
    assert selection.modifiers["values"] == "J:1,O:7,H:5,N:5"
    assert reading.summary == "Name number 9 (Mars); total 18."


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("John")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "system=chaldean" in reading.provenance.notes
    assert "value_system=latin_chaldean.v1" in reading.provenance.notes


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CHALDEAN_NUMEROLOGY_SPREAD.id, deck_id=CHALDEAN_NUMEROLOGY_DECK.id
            )
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "chaldean_numerology" not in fortune_telling_core.__all__


def _request(name: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=CHALDEAN_NUMEROLOGY_SPREAD.id,
        deck_id=CHALDEAN_NUMEROLOGY_DECK.id,
        querent=Querent("native", "Native", {"name": name}),
    )
