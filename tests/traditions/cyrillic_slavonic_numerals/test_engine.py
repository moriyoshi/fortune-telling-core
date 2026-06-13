import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.cyrillic_slavonic_numerals import (
    CYRILLIC_SLAVONIC_NUMERALS_DECK,
    CYRILLIC_SLAVONIC_NUMERALS_SPREAD,
    build_engine,
)


def test_cast_records_total_and_structural_summary() -> None:
    reading = build_engine().cast(_request("арі"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "total"
    assert selection.symbol_id == "cyrillic_slavonic_numerals.result.total"
    assert selection.modifiers is not None
    assert selection.modifiers["total"] == "111"
    assert selection.modifiers["value"] == "111"
    assert selection.modifiers["values"] == "а:1,р:100,і:10"
    assert selection.modifiers["value_system"] == "cyrillic_slavonic_numerals.v1"
    assert selection.modifiers["letter_table"] == "common_church_slavonic"
    assert selection.modifiers["titlo"] == "optional"
    assert reading.summary == "Old Cyrillic numeral total 111."


def test_variant_option_records_provenance() -> None:
    reading = build_engine().cast(_request("чҁ", koppa_mode="koppa_90", xi_mode="cherv_60"))
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None
    assert modifiers["total"] == "150"
    assert "koppa_mode=koppa_90" in reading.provenance.notes
    assert "xi_mode=cherv_60" in reading.provenance.notes


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("арі")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_provenance_stamps_system_and_value_system() -> None:
    reading = build_engine().cast(_request("арі"))
    assert "system=cyrillic_slavonic_numerals" in reading.provenance.notes
    assert "value_system=cyrillic_slavonic_numerals.v1" in reading.provenance.notes
    assert "letter_table=common_church_slavonic" in reading.provenance.notes


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CYRILLIC_SLAVONIC_NUMERALS_SPREAD.id,
                deck_id=CYRILLIC_SLAVONIC_NUMERALS_DECK.id,
            )
        )


def test_validation_error_on_unvalued_letter() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("ѣ"))


def test_validation_error_on_bad_option() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("арі", koppa_mode="bad"))


def _request(name: str, **options: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=CYRILLIC_SLAVONIC_NUMERALS_SPREAD.id,
        deck_id=CYRILLIC_SLAVONIC_NUMERALS_DECK.id,
        querent=Querent("native", "Native", {"name": name}),
        options=options or None,
    )
