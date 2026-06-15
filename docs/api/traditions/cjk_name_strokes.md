# CJK Name Stroke Onomancy

A CJK five-grid (Japanese *seimei-handan* 姓名判断 / Chinese 五格剖象) engine that
computes the heaven, person, earth, outer, and total grids from the brush-stroke
counts of a name's characters, using the standard 熊崎式 formulas (including the
single-character 霊数 "spirit number" rule). The selected `school` and
`character_set` are recorded for provenance.

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
    options={"surname": "山田", "given_name": "太郎"},
)
reading = build_engine().cast(request)
# reading.summary -> "CJK name stroke total 20; heaven 8; person 9; earth 12; outer 11."
```

## Stroke sources

Every character needs a stroke count, supplied by a **stroke-count provider**.
The `stroke_source` option names the provider to use (default `"unihan"`);
providers are looked up in a registry. The resolved per-character counts and the
provider's id/version are recorded on the reading (`values`, `value_system`)
so a reading is reproducible and auditable.

### Bundled Unihan table (`unihan`, the default)

By default counts come from the bundled Unicode Unihan `kTotalStrokes` table —
no preparation is needed (the example above uses it). These are
*representative-glyph* totals per Unicode UAX #38, **not** the Kangxi / old-form
counts that some *seimei-handan* schools require; the reading records
`value_system=cjk_unihan_strokes.v1` so the basis is explicit.

!!! warning "Unihan counts can differ from a school's"
    A character's stroke count is glyph-dependent, and Unihan records the count
    for its *representative* glyph. For example **郎 (U+90CE)** is **8** in
    Unihan but **9** in the Japanese tradition (KANJIDIC lists "9, also 8"), so
    `田中太郎` totals **20** under the Unihan default versus **21** under the
    *seimei-handan* count. Where Unihan lists two values (zh-Hans then zh-Hant),
    the bundled table keeps the first. For tradition-faithful counts, register a
    provider (below) using the convention your school expects.

### Third-party dataset (a registered provider)

For school-specific or higher-fidelity counts, register your own provider. **The
library bundles no third-party data** — KANJIDIC2 and KanjiVG are share-alike
(CC BY-SA), whose ShareAlike terms preclude redistributing them here — so you
obtain the data yourself and comply with its licence. The library ships parsers
for two common formats.

**1. Obtain the dataset** (and follow its licence terms):

- **KANJIDIC2** — EDRDG, CC BY-SA 4.0 — <https://www.edrdg.org/wiki/index.php/KANJIDIC_Project>
  (download `kanjidic2.xml.gz` and decompress it). Modern Japanese (shinjitai) counts.
- **KanjiVG** — CC BY-SA 3.0 — <https://kanjivg.tagaini.net/> (the aggregated
  `kanjivg-*.xml`, or per-character SVGs). Counts are derived by counting stroke paths.

**2. Parse it into a `{character: stroke_count}` mapping**, wrap it in a
`MappingStrokeProvider` (its id/version are recorded as the reading's value
system), and register it under a name:

```python
from fortune_telling_core.traditions.cjk_name_strokes import (
    MappingStrokeProvider,
    parse_kanjidic2,
    register_provider,
)

with open("kanjidic2.xml", "rb") as fh:
    table = parse_kanjidic2(fh)   # {"山": 3, "田": 5, ...}
register_provider(MappingStrokeProvider("kanjidic2", "2024-01", table))
```

**3. Select the provider by name via `stroke_source`:**

```python
request = ReadingRequest(
    deck_id=CJK_NAME_STROKES_DECK.id,
    spread_id=CJK_NAME_STROKES_SPREAD.id,
    options={"surname": "山田", "given_name": "太郎", "stroke_source": "kanjidic2"},
)
reading = build_engine().cast(request)
# provenance notes include: stroke_source=kanjidic2, value_system=kanjidic2
```

`register_provider` adds to a process-wide default registry. To avoid global
state (e.g. in tests or a multi-tenant app), build a private registry instead
and inject it:

```python
from fortune_telling_core.traditions.cjk_name_strokes import new_default_registry

registry = new_default_registry()  # seeded with "unihan"
registry.register(MappingStrokeProvider("kanjidic2", "2024-01", table), name="kanjidic2")
reading = build_engine(registry=registry).cast(request)
```

Any object satisfying the `StrokeCountProvider` protocol (`id`, `version`,
`stroke_count(char) -> int | None`) can be registered, so a school table with
its own Kangxi/radical-restoration rules plugs in the same way. `parse_kanjidic2`
/ `parse_kanjivg` produce literal, as-printed counts without radical restoration,
so — like the bundled Unihan table — they are not faithful to Kangxi-based
schools.

::: fortune_telling_core.traditions.cjk_name_strokes
