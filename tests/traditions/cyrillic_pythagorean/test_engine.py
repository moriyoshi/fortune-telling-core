import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.cyrillic_pythagorean import (
    CYRILLIC_PYTHAGOREAN_DECK,
    CYRILLIC_PYTHAGOREAN_SPREAD,
    build_engine,
)


def test_cast_records_root_and_structural_summary() -> None:
    reading = build_engine().cast(_request("Иван"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "name_number"
    assert selection.symbol_id == "cyrillic_pythagorean.number.2"
    assert selection.modifiers is not None
    assert selection.modifiers["total"] == "11"
    assert selection.modifiers["value"] == "2"
    assert selection.modifiers["values"] == "и:1,в:3,а:1,н:6"
    assert selection.modifiers["value_system"] == "cyrillic_pythagorean.v1"
    assert selection.modifiers["language"] == "russian"
    assert selection.modifiers["alphabet"] == "russian_33"
    assert selection.modifiers["yo_mode"] == "distinct"
    assert reading.summary == "Cyrillic Pythagorean root 2 from total 11."


def test_variant_option_records_provenance() -> None:
    reading = build_engine().cast(
        _request("ёлка", alphabet="russian_32_no_yo", yo_mode="fold_to_e")
    )
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None
    assert modifiers["normalized_name"].startswith("е")
    assert "alphabet=russian_32_no_yo" in reading.provenance.notes
    assert "yo_mode=fold_to_e" in reading.provenance.notes


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("Иван")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_provenance_stamps_system_and_value_system() -> None:
    reading = build_engine().cast(_request("Иван"))
    assert "system=cyrillic_pythagorean" in reading.provenance.notes
    assert "value_system=cyrillic_pythagorean.v1" in reading.provenance.notes
    assert "normalization=strict_cyrillic" in reading.provenance.notes


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CYRILLIC_PYTHAGOREAN_SPREAD.id,
                deck_id=CYRILLIC_PYTHAGOREAN_DECK.id,
            )
        )


def test_validation_error_on_non_cyrillic_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("John"))


def test_validation_error_on_bad_option() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("Иван", language="latin"))


def _request(name: str, **options: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=CYRILLIC_PYTHAGOREAN_SPREAD.id,
        deck_id=CYRILLIC_PYTHAGOREAN_DECK.id,
        querent=Querent("native", "Native", {"name": name}),
        options=options or None,
    )
