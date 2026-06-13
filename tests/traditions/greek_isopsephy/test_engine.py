import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.greek_isopsephy import (
    GREEK_ISOPSEPHY_DECK,
    GREEK_ISOPSEPHY_SPREAD,
    build_engine,
)


def test_cast_records_total_and_structural_summary() -> None:
    reading = build_engine().cast(_request("Αλφα"))

    selection = reading.draw.selections[0]
    assert selection.position_id == "total"
    assert selection.symbol_id == "greek_isopsephy.result.total"
    assert selection.modifiers is not None
    assert selection.modifiers["total"] == "532"
    assert selection.modifiers["value"] == "532"
    assert selection.modifiers["values"] == "α:1,λ:30,φ:500,α:1"
    assert selection.modifiers["value_system"] == "greek_isopsephy.v1"
    assert selection.modifiers["era"] == "classical"
    assert selection.modifiers["diacritics"] == "stripped"
    assert selection.modifiers["sigma_mode"] == "final_to_sigma"
    assert reading.summary == "Isopsephy total 532."


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request("λόγος")
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_provenance_stamps_system_and_value_system() -> None:
    reading = build_engine().cast(_request("λόγος"))
    assert "system=greek_isopsephy" in reading.provenance.notes
    assert "value_system=greek_isopsephy.v1" in reading.provenance.notes
    assert "diacritics=stripped" in reading.provenance.notes
    assert "sigma_mode=final_to_sigma" in reading.provenance.notes


def test_validation_error_on_missing_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=GREEK_ISOPSEPHY_SPREAD.id, deck_id=GREEK_ISOPSEPHY_DECK.id)
        )


def test_validation_error_on_non_greek_name() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("John"))


def test_validation_error_on_bad_option() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request("λόγος", sigma_mode="drop"))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "greek_isopsephy" not in fortune_telling_core.__all__


def _request(name: str, **options: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=GREEK_ISOPSEPHY_SPREAD.id,
        deck_id=GREEK_ISOPSEPHY_DECK.id,
        querent=Querent("native", "Native", {"name": name}),
        options=options or None,
    )
