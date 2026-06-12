import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.name_numerology import (
    NAME_NUMEROLOGY_DECK,
    NAME_NUMEROLOGY_SPREAD,
    YMode,
    build_engine,
)


def test_cast_records_core_numbers_and_summary() -> None:
    reading = build_engine().cast(_request({"name": "John"}))

    assert tuple(s.position_id for s in reading.draw.selections) == (
        "expression",
        "soul_urge",
        "personality",
    )
    expression = reading.draw.selections[0]
    assert expression.symbol_id == "name_numerology.number.2"
    assert expression.modifiers is not None
    assert expression.modifiers["keyword"] == "Diplomat"
    assert reading.summary == (
        "Expression 2 (Diplomat); Soul Urge 6 (Nurturer); Personality 5 (Freedom)."
    )


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request({"name": "John"})
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "y_mode=consonant" in reading.provenance.notes
    assert "system=pythagorean" in reading.provenance.notes


def test_request_y_mode_override_changes_personality() -> None:
    reading = build_engine().cast(_request({"name": "Amy", "y_mode": "vowel"}))

    assert reading.draw.selections[1].symbol_id == "name_numerology.number.8"  # Soul Urge
    assert reading.draw.selections[2].symbol_id == "name_numerology.number.4"  # Personality
    assert "y_mode=vowel" in reading.provenance.notes


def test_engine_default_y_mode_applies() -> None:
    reading = build_engine(y_mode=YMode.VOWEL).cast(_request({"name": "Amy"}))

    assert reading.draw.selections[1].symbol_id == "name_numerology.number.8"


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=NAME_NUMEROLOGY_SPREAD.id, deck_id=NAME_NUMEROLOGY_DECK.id)
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "name_numerology" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str]) -> ReadingRequest:
    return ReadingRequest(
        spread_id=NAME_NUMEROLOGY_SPREAD.id,
        deck_id=NAME_NUMEROLOGY_DECK.id,
        querent=Querent("native", "Native", attrs),
    )
