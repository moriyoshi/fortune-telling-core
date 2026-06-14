# CJK Name Stroke Onomancy

A CJK five-grid (Japanese *seimei-handan* 姓名判断 / Chinese 五格剖象) engine that
computes the heaven, person, earth, outer, and total grids from the brush-stroke
counts of a name's characters, using the standard 熊崎式 formulas (including the
single-character 霊数 "spirit number" rule). Stroke counts are **caller-supplied**
via the `strokes` option — the library bundles no stroke database — and the
selected `school` and `character_set` are recorded for provenance.

```python
from fortune_telling_core import ReadingRequest
from fortune_telling_core.traditions.cjk_name_strokes import (
    CJK_NAME_STROKES_DECK,
    CJK_NAME_STROKES_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=CJK_NAME_STROKES_DECK.id,
    spread_id=CJK_NAME_STROKES_SPREAD.id,
    options={
        "surname": "山田",
        "given_name": "太郎",
        "strokes": "山:3,田:5,太:4,郎:9",
    },
)
reading = build_engine().cast(request)
# reading.summary -> "CJK name stroke total 21; heaven 8; person 9; earth 13; outer 12."
```

::: fortune_telling_core.traditions.cjk_name_strokes
