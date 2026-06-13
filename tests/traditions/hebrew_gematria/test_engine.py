import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.hebrew_gematria import (
    HEBREW_GEMATRIA_DECK,
    HEBREW_GEMATRIA_SPREAD,
    build_engine,
)


def test_cast_records_total_and_structural_summary() -> None:
    reading = build_engine().cast(_request("חיים"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "total"
    assert selection.symbol_id == "hebrew_gematria.result.total"
    assert selection.modifiers is not None
    assert selection.modifiers["total"] == "68"
    assert selection.modifiers["value"] == "68"
    assert selection.modifiers["values"] == "ח:8,י:10,י:10,ם:40"
    assert selection.modifiers["value_system"] == "hebrew_gematria.v1"
    assert selection.modifiers["final_letter_mode"] == "standard"
    assert reading.summary == "Gematria total 68."


def test_gadol_mode_via_option() -> None:
    reading = build_engine().cast(_request("חיים", final_letter_mode="gadol"))
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None
    # final mem 40 -> 600, so 8 + 10 + 10 + 600 = 628.
    assert modifiers["total"] == "628"
    assert "final_letters=gadol" in reading.provenance.notes


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("שלום")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_provenance_stamps_system_and_value_system() -> None:
    reading = build_engine().cast(_request("שלום"))
    assert "system=hebrew_gematria" in reading.provenance.notes
    assert "value_system=hebrew_gematria.v1" in reading.provenance.notes
    assert "vowels=ignored" in reading.provenance.notes


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=HEBREW_GEMATRIA_SPREAD.id, deck_id=HEBREW_GEMATRIA_DECK.id)
        )


def test_validation_error_on_non_hebrew_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("John"))


def test_validation_error_on_bad_final_letter_mode() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("שלום", final_letter_mode="huge"))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "hebrew_gematria" not in fortune_telling_core.__all__


def _request(name: str, **options: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=HEBREW_GEMATRIA_SPREAD.id,
        deck_id=HEBREW_GEMATRIA_DECK.id,
        querent=Querent("native", "Native", {"name": name}),
        options=options or None,
    )
