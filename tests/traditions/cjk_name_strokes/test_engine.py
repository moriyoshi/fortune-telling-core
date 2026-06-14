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
    CjkNameStrokesEngine,
    MappingStrokeProvider,
    StrokeProviderRegistry,
    build_engine,
    new_default_registry,
)

_SCHOOL_COUNTS = {"山": 3, "田": 5, "太": 4, "郎": 9}


def _engine_with_provider(
    name: str = "kanjidic2", *, version: str = "2024-01"
) -> CjkNameStrokesEngine:
    registry = new_default_registry()
    registry.register(MappingStrokeProvider(name, version, _SCHOOL_COUNTS), name=name)
    return build_engine(registry=registry)


def _request(**options: str) -> ReadingRequest:
    opts = {"surname": "山田", "given_name": "太郎"}
    opts.update(options)
    return ReadingRequest(
        spread_id=CJK_NAME_STROKES_SPREAD.id,
        deck_id=CJK_NAME_STROKES_DECK.id,
        querent=Querent("native", "Native", {}),
        options=opts,
    )


def test_cast_records_five_grid_and_resolved_counts_on_total_selection() -> None:
    reading = _engine_with_provider().cast(_request(stroke_source="kanjidic2"))

    selections = {selection.position_id: selection for selection in reading.draw.selections}
    total = selections["total"].modifiers
    assert total is not None
    assert total["total"] == "21"
    assert total["value"] == "21"
    assert total["heaven"] == "8"
    assert total["person"] == "9"
    assert total["earth"] == "13"
    assert total["outer"] == "12"
    # The resolved per-character stroke counts are recorded on the reading.
    assert total["characters"] == "山田太郎"
    assert total["values"] == "山:3,田:5,太:4,郎:9"
    assert total["value_system"] == "kanjidic2"
    assert total["value_system_version"] == "2024-01"
    assert total["stroke_source"] == "kanjidic2"

    for position in ("heaven", "person", "earth", "outer"):
        modifiers = selections[position].modifiers
        assert modifiers is not None
        assert modifiers["trace_position"] == "total"

    assert reading.summary == "CJK name stroke total 21; heaven 8; person 9; earth 13; outer 12."


def test_unihan_table_is_the_default_source() -> None:
    reading = build_engine().cast(_request())
    total = reading.draw.selections[-1].modifiers
    assert total is not None
    assert total["stroke_source"] == "unihan"
    assert total["value_system"] == "cjk_unihan_strokes.v1"
    assert total["values"] == "山:3,田:5,太:4,郎:8"  # Unihan 郎 = 8
    assert total["total"] == "20"
    assert "stroke_source=unihan" in reading.provenance.notes
    assert "value_system=cjk_unihan_strokes.v1" in reading.provenance.notes


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
    # Unihan: 山 = 3, 太 = 4.
    reading = build_engine().cast(_request(surname="山", given_name="太"))
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
    assert "value_system=cjk_unihan_strokes.v1" in reading.provenance.notes
    assert "stroke_source=unihan" in reading.provenance.notes
    assert "grid=five_grid" in reading.provenance.notes


def test_validation_error_on_missing_name_parts() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CJK_NAME_STROKES_SPREAD.id,
                deck_id=CJK_NAME_STROKES_DECK.id,
            )
        )


def test_validation_error_on_unknown_stroke_source() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request(stroke_source="does_not_exist"))


def test_validation_error_when_provider_lacks_a_character() -> None:
    registry = StrokeProviderRegistry()
    registry.register(MappingStrokeProvider("partial", "1", {"山": 3, "田": 5}), name="partial")
    with pytest.raises(ValidationError):
        build_engine(registry=registry).cast(_request(stroke_source="partial"))
