import io

import pytest

from fortune_telling_core import Querent, ReadingRequest, ValidationError
from fortune_telling_core.traditions.cjk_name_strokes import (
    CJK_NAME_STROKES_DECK,
    CJK_NAME_STROKES_SPREAD,
    MappingStrokeProvider,
    build_engine,
    new_default_registry,
    parse_kanjidic2,
    parse_kanjivg,
)

# Minimal hand-authored samples in each format (not third-party data).
_KANJIDIC2 = b"""<?xml version="1.0" encoding="UTF-8"?>
<kanjidic2>
  <character>
    <literal>\xe5\xb1\xb1</literal>
    <misc>
      <grade>1</grade>
      <stroke_count>3</stroke_count>
    </misc>
  </character>
  <character>
    <literal>\xe7\x94\xb0</literal>
    <misc>
      <stroke_count>5</stroke_count>
      <stroke_count>6</stroke_count>
    </misc>
  </character>
</kanjidic2>
"""

# 山 = three strokes; the StrokeNumbers <text> nodes must be ignored.
_KANJIVG_SVG = b"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:kvg="http://kanjivg.tagaini.net">
  <g id="kvg:StrokePaths_05c71">
    <g id="kvg:05c71" kvg:element="\xe5\xb1\xb1">
      <path id="kvg:05c71-s1" d="M0,0"/>
      <path id="kvg:05c71-s2" d="M1,1"/>
      <path id="kvg:05c71-s3" d="M2,2"/>
    </g>
  </g>
  <g id="kvg:StrokeNumbers_05c71">
    <text>1</text><text>2</text><text>3</text>
  </g>
</svg>
"""


def test_parse_kanjidic2_takes_first_stroke_count() -> None:
    table = parse_kanjidic2(io.BytesIO(_KANJIDIC2))
    assert table == {"山": 3, "田": 5}


def test_parse_kanjidic2_rejects_character_without_stroke_count() -> None:
    bad = b"<kanjidic2><character><literal>\xe5\xb1\xb1</literal></character></kanjidic2>"
    with pytest.raises(ValidationError):
        parse_kanjidic2(io.BytesIO(bad))


def test_parse_kanjivg_counts_paths_and_ignores_stroke_numbers() -> None:
    table = parse_kanjivg(io.BytesIO(_KANJIVG_SVG))
    assert table == {"山": 3}


def test_parsed_table_feeds_engine_through_a_registered_provider() -> None:
    table = parse_kanjidic2(io.BytesIO(_KANJIDIC2))
    table["太"] = 4
    table["郎"] = 9
    registry = new_default_registry()
    registry.register(MappingStrokeProvider("kanjidic2", "2024-01", table), name="kanjidic2")

    reading = build_engine(registry=registry).cast(
        ReadingRequest(
            spread_id=CJK_NAME_STROKES_SPREAD.id,
            deck_id=CJK_NAME_STROKES_DECK.id,
            querent=Querent("native", "Native", {}),
            options={"surname": "山田", "given_name": "太郎", "stroke_source": "kanjidic2"},
        )
    )

    total = reading.draw.selections[-1].modifiers
    assert total is not None
    assert total["stroke_source"] == "kanjidic2"
    assert total["value_system"] == "kanjidic2"
    assert total["value_system_version"] == "2024-01"
    # The reading carries the resolved per-character stroke counts.
    assert total["characters"] == "山田太郎"
    assert total["values"] == "山:3,田:5,太:4,郎:9"
    assert "stroke_source=kanjidic2" in reading.provenance.notes


def test_unknown_stroke_source_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(
                spread_id=CJK_NAME_STROKES_SPREAD.id,
                deck_id=CJK_NAME_STROKES_DECK.id,
                querent=Querent("native", "Native", {}),
                options={"surname": "山", "given_name": "田", "stroke_source": "kanjidic2"},
            )
        )
