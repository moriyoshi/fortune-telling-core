import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.cjk_name_strokes import (
    CJK_NAME_STROKES_DECK,
    CJK_NAME_STROKES_SPREAD,
    build_engine,
)


def test_cast_records_five_grid_and_trace_on_total_selection() -> None:
    reading = build_engine().cast(_request())

    selections = {selection.position_id: selection for selection in reading.draw.selections}
    total = selections["total"].modifiers
    assert total is not None
    assert total["total"] == "21"
    assert total["value"] == "21"
    assert total["heaven"] == "8"
    assert total["person"] == "9"
    assert total["earth"] == "13"
    assert total["outer"] == "12"
    assert total["characters"] == "山田太郎"
    assert total["values"] == "山:3,田:5,太:4,郎:9"
    assert total["value_system"] == "cjk_name_strokes.request.v1"
    assert total["stroke_source"] == "request"

    for position in ("heaven", "person", "earth", "outer"):
        modifiers = selections[position].modifiers
        assert modifiers is not None
        assert modifiers["trace_position"] == "total"

    assert reading.summary == "CJK name stroke total 21; heaven 8; person 9; earth 13; outer 12."


def test_option_values_are_recorded() -> None:
    reading = build_engine().cast(
        _request(school="chinese_xingmingxue", character_set="traditional")
    )
    total = reading.draw.selections[-1].modifiers
    assert total is not None
    assert total["school"] == "chinese_xingmingxue"
    assert total["character_set"] == "traditional"
    assert "school=chinese_xingmingxue" in reading.provenance.notes
    assert "character_set=traditional" in reading.provenance.notes


def test_single_character_name_parts_use_virtual_strokes() -> None:
    reading = build_engine().cast(
        _request(
            surname="山",
            given_name="太",
            strokes="山:3,太:4",
        )
    )
    total = reading.draw.selections[-1].modifiers
    assert total is not None
    assert total["total"] == "7"
    assert total["heaven"] == "4"
    assert total["person"] == "7"
    assert total["earth"] == "5"
    assert total["outer"] == "2"


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_provenance_stamps_system_and_value_system() -> None:
    reading = build_engine().cast(_request())
    assert "system=cjk_name_strokes" in reading.provenance.notes
    assert "value_system=cjk_name_strokes.request.v1" in reading.provenance.notes
    assert "stroke_source=request" in reading.provenance.notes
    assert "grid=five_grid" in reading.provenance.notes


def test_validation_error_on_missing_name_parts() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CJK_NAME_STROKES_SPREAD.id,
                deck_id=CJK_NAME_STROKES_DECK.id,
            )
        )


def test_validation_error_on_missing_stroke_count() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request(strokes="山:3,田:5,太:4"))


def test_validation_error_on_bad_option() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request(stroke_source="unicode"))


def _request(**options: str) -> ReadingRequest:
    default_options = {
        "surname": "山田",
        "given_name": "太郎",
        "strokes": "山:3,田:5,太:4,郎:9",
    }
    default_options.update(options)
    return ReadingRequest(
        spread_id=CJK_NAME_STROKES_SPREAD.id,
        deck_id=CJK_NAME_STROKES_DECK.id,
        querent=Querent("native", "Native", {}),
        options=default_options,
    )
