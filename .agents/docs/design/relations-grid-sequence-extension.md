# Relations, Grid, and Sequence Extension Proposal

Status: Proposal only

Related item: TODO #47, "Consider a future first-class core relations, grid, or sequence extension for aspects, luck pillars, and Lo Shu charts."

## Problem

The current core reading model has strong primitives for the request, spread, draw, resolved positions, provenance, and optional summary text. It does not yet have first-class structural primitives for relationships between positions, ordered derived runs, or two-dimensional charts.

As a result, several computed traditions serialize durable derived structures as plain `Reading.summary` text:

- Astrology computes aspects from stamped longitude modifiers and renders them as text with `render_aspects(compute_aspects(...))`.
- Four Pillars computes element balance, Day Master strength, Luck Pillars, and the annual pillar from selection modifiers and renders them into summary text.
- Nine Star Ki stamps annual and monthly Lo Shu flying-star chart renderings into selection modifiers, then renders those strings into summary text.

This works for replay because the necessary scalar values are already stamped into `Draw.selections[*].modifiers`, but it is weak for downstream consumers. A UI, API client, or interpretation harness must parse English summary text or duplicate tradition-specific derivation logic to inspect aspects, luck-pillar timelines, or palace grids.

## Goals

- Preserve the current deterministic, replayable model.
- Keep `Reading.summary` working for existing consumers.
- Add a small, generic structural layer that can express relations, ordered sequences, and grids without baking in tradition-specific interpretation.
- Keep primitives typed and serializable, but avoid turning the core into a localization or meaning-text system.
- Make derived structures auditable by recording the calculation method, source positions, and important options in structured data and provenance.

## Non-Goals

- Do not move human interpretation text back into the core.
- Do not replace `Draw`, `Selection`, `Spread`, or `PositionReading`.
- Do not require every engine to emit the new structures.
- Do not model every possible astrological, BaZi, or Nine Star Ki variant upfront.
- Do not remove summary text during the migration.

## Proposed Core Primitives

Add an optional structural extension to `Reading`, tentatively named `structures`, containing zero or more typed artifacts. The artifacts should be data-only value objects with stable `to_dict` and `from_dict` methods.

### Structure

`Structure` is a tagged union wrapper:

```python
Relation | Sequence | Grid
```

Each structure should carry:

- `id`: Stable per-reading identifier, such as `astrology.aspects` or `nine_star_ki.annual_chart`.
- `kind`: One of `relation`, `sequence`, or `grid`.
- `label`: Optional short display label in plain American English.
- `system`: Optional tradition or subsystem id, such as `astrology`, `four_pillars`, or `nine_star_ki`.
- `source`: Optional source references to `position_id`, `symbol_id`, or modifier keys used to derive the structure.
- `metadata`: String-keyed scalar metadata for calculation options and audit values.

`metadata` should remain small and serializable. Use strings, numbers, booleans, nulls, and arrays or objects only when the schema defines them explicitly.

### Relation

`Relation` represents a typed connection between two or more reading entities.

Suggested shape:

```python
Relation(
    id: str,
    relation_type: str,
    endpoints: tuple[Endpoint, ...],
    values: Mapping[str, Scalar],
    label: str | None = None,
    system: str | None = None,
    source: tuple[SourceRef, ...] = (),
    metadata: Mapping[str, Scalar] = {},
)
```

`Endpoint` should reference existing reading entities rather than duplicating them:

- `role`: `first`, `second`, `subject`, `object`, `palace`, etc.
- `position_id`: Optional spread position id.
- `symbol_id`: Optional selected symbol id.
- `locator`: Optional extra locator for non-spread entities, such as a Lo Shu palace.

Use `values` for measured or computed values:

- Astrology aspect angle, orb, applying/separating if supported later.
- Four Pillars relation values such as Ten God links or element interactions if added later.
- Nine Star Ki palace-to-star or natal-to-current comparisons if added later.

### Sequence

`Sequence` represents an ordered derived series. It is suited to time runs, cycles, progressions, and reusable ordered chart paths.

Suggested shape:

```python
Sequence(
    id: str,
    sequence_type: str,
    items: tuple[SequenceItem, ...],
    label: str | None = None,
    system: str | None = None,
    source: tuple[SourceRef, ...] = (),
    metadata: Mapping[str, Scalar] = {},
)
```

`SequenceItem` should carry:

- `index`: Zero-based stable order within the sequence.
- `key`: Optional stable item key.
- `symbol_id`: Optional symbol represented by this item.
- `position_id`: Optional related position.
- `label`: Optional short display label.
- `starts_at`: Optional ISO date or datetime when a real time boundary is known.
- `start_age`: Optional numeric age when the tradition works in age offsets.
- `duration`: Optional structured duration, such as `{"years": 10}`.
- `values`: Additional typed scalar values, such as `cycle_index`, `cjk`, or `direction`.

### Grid

`Grid` represents a stable arrangement of cells. It should support Lo Shu-style directional palaces without requiring a rectangular matrix for all traditions.

Suggested shape:

```python
Grid(
    id: str,
    grid_type: str,
    cells: tuple[GridCell, ...],
    label: str | None = None,
    system: str | None = None,
    layout: GridLayout | None = None,
    source: tuple[SourceRef, ...] = (),
    metadata: Mapping[str, Scalar] = {},
)
```

`GridCell` should carry:

- `key`: Stable cell id, such as `NW`, `N`, `NE`, `W`, `C`, `E`, `SW`, `S`, `SE`.
- `row`: Optional display row.
- `column`: Optional display column.
- `symbol_id`: Optional selected or derived symbol id.
- `label`: Optional short display label.
- `values`: Cell values such as star number, palace, home palace, element, trigram, or flight index.

`GridLayout` should describe display and traversal:

- `layout_type`: `lo_shu`, `rectangular`, or another stable id.
- `rows`: Optional row count.
- `columns`: Optional column count.
- `order`: Optional tuple of cell keys for canonical traversal.

For Lo Shu, the display layout can be the current rendered order:

```text
NW N NE
W  C E
SW S SE
```

The flight order can live in metadata or as a separate `Sequence` when consumers need traversal semantics:

```text
C, NW, W, NE, S, N, SW, E, SE
```

## Tradition Mappings

### Astrology Aspects

Current behavior:

- `chart.cast_draw` stamps each body or angle selection with `longitude`, `degree`, `house`, `speed`, and `retrograde`.
- `AstrologyEngine._interpret` collects longitudes from positions included in aspects.
- `compute_aspects` compares each pair, skips the north-node/south-node pair, matches the first default aspect within orb, and returns `Aspect(first, second, definition, orb)`.
- `render_aspects` turns those aspects into a semicolon-delimited summary sentence.

Proposed structure:

- Emit one `Relation` per aspect, grouped under a container id such as `astrology.aspects`.
- `relation_type`: the aspect id, such as `conjunction`, `opposition`, `trine`, `square`, or `sextile`.
- `endpoints`: two endpoints referencing the aspecting `position_id`s and their selected `symbol_id`s.
- `values`:
  - `angle`: exact aspect angle from `AspectDef.angle`.
  - `orb`: computed orb in degrees.
  - `max_orb`: allowed orb from `AspectDef.orb`.
  - `actual_distance`: optional angular distance if the engine chooses to expose it.
- `metadata`:
  - `aspect_set`: `default`.
  - `include_angles`: boolean reflecting the request config.
  - `zodiac`: copied from provenance or request config.
  - `house_system`: copied from provenance or request config.

This makes aspects inspectable without parsing text while keeping the existing summary sentence as a rendering of the same relation list.

### Four Pillars Luck Pillars and Annual Pillar

Current behavior:

- `chart.draw_from_pillars` stamps cycle data on every stem and branch selection.
- The day stem selection also carries `luck_direction`, `luck_start_age`, `month_cycle_index`, `luck_count`, and `target_year`.
- `_summary_from_draw` recomputes element distribution and Day Master strength, rebuilds Luck Pillars via `luck_pillars`, and renders the annual pillar via `annual_pillar_cjk(target_year)`.

Proposed structures:

- Emit a `Sequence` with id `four_pillars.luck_pillars`.
- `sequence_type`: `luck_pillars`.
- `items`: one item per luck pillar.
- Each item should include:
  - `index`: the current `LuckPillar.index`.
  - `start_age`: the current `LuckPillar.start_age`.
  - `duration`: `{"years": 10}`.
  - `values.cycle_index`: the sexagenary cycle index.
  - `values.cjk`: the current CJK ganzhi label.
  - `values.direction`: `forward` or `backward`.
- `source`: references the day stem modifier keys used to derive the sequence.
- `metadata`:
  - `month_cycle_index`.
  - `luck_direction`.
  - `luck_start_age`.
  - `luck_count`.
  - `time_model`.
  - `day_boundary`.

For the annual pillar, there are two reasonable options:

- A single-item `Sequence` with id `four_pillars.annual_pillar` and `sequence_type` `annual_pillar`.
- A `Relation` between `target_year` and the derived sexagenary symbol.

The single-item `Sequence` is preferable because annual pillars naturally generalize to a multi-year annual sequence without changing the shape. The first implementation can emit only the requested target year:

- `key`: the target year as a string.
- `values.year`: target year.
- `values.cycle_index`: optional, if exposed by the helper rather than only CJK text.
- `values.cjk`: annual pillar label.

Element distribution and Day Master strength could remain summary-only initially or become future structures:

- Element distribution: a compact `Grid` is not a natural fit; a future `MetricSet` may be better.
- Day Master strength: a scalar derived assessment; keep in summary until a general scalar artifact exists.

### Nine Star Ki Lo Shu and Flying-Star Charts

Current behavior:

- `compute_chart` calculates principal, monthly, daily, tendency, target year, and annual star values.
- `chart.draw_from_chart` stamps these values into every selection.
- It also renders `annual_chart` and `monthly_chart` as text by calling `render_chart(fly_chart(center_star))`.
- `_summary_from_draw` copies those rendered chart strings into `Reading.summary`.

Proposed structures:

- Emit a `Grid` with id `nine_star_ki.annual_chart`.
- Emit a `Grid` with id `nine_star_ki.monthly_chart`.
- `grid_type`: `lo_shu_flying_star`.
- `layout`: `layout_type="lo_shu"`, `rows=3`, `columns=3`, and order `("NW", "N", "NE", "W", "C", "E", "SW", "S", "SE")`.
- Each `GridCell` should include:
  - `key`: palace id.
  - `row` and `column` matching the current render layout.
  - `symbol_id`: `nsk.star.{number}`.
  - `values.star`: the star number.
  - `values.palace`: the palace id.
  - `values.flight_index`: the index in `FLIGHT_ORDER`.
  - Optional star metadata already available from `stars.py`: element, trigram, color, CJK, home palace.
- `metadata`:
  - For annual chart: `target_year`, `annual_star`, `center_star`.
  - For monthly chart: `solar_month_index`, `month_star`, `center_star`.
  - For both: `flight_order`, `year_anchor`, `day_star_escapement`, and `time_model` where relevant.

If consumers need the flying path independently from the rendered grid, emit a companion `Sequence`:

- `id`: `nine_star_ki.flight_order`.
- `sequence_type`: `grid_traversal`.
- Items reference the same palace keys in `FLIGHT_ORDER`.

The current principal, monthly, daily, and tendency star placements should remain normal `PositionReading` entries because they are spread positions, not derived grid cells.

## Serialization and Replay

The extension should preserve the current replay contract:

- `Draw` remains the authoritative replay artifact.
- `Reading.structures` is derived by `interpret` and `replay` from `Draw`, request options, engine defaults, and provenance-relevant configuration.
- Computed engines should not need an ephemeris during replay if all required values are already stamped into modifiers.

For structures to be replay-stable:

- Structure ids and item ids must be deterministic.
- Floating values should use the same precision rules as existing modifiers or documented numeric precision in JSON.
- Any configurable school or calculation choice that changes a structure must be present in `Provenance.notes` and/or the structure metadata.
- Derived values that cannot be reconstructed from `Draw` without an ephemeris should be stamped into selection modifiers before the structure is built.

Schema options:

- Keep `schema_version` compatible by making `structures` optional. Old readings without `structures` still deserialize.
- Add a minor schema note or bump only if the project treats new top-level fields as a versioned schema change.
- Unknown future structure kinds should raise validation errors in strict deserialization, but consumers can still ignore the optional top-level field if they do not need it.

Suggested JSON shape:

```json
{
  "structures": [
    {
      "kind": "relation",
      "id": "astrology.aspect.0",
      "system": "astrology",
      "relation_type": "trine",
      "endpoints": [
        {"role": "first", "position_id": "sun", "symbol_id": "zodiac.aries"},
        {"role": "second", "position_id": "moon", "symbol_id": "zodiac.leo"}
      ],
      "values": {"angle": 120.0, "orb": 1.25, "max_orb": 6.0}
    }
  ]
}
```

## Migration Path

1. Add the value objects and optional `Reading.structures` field with default empty tuple semantics.
2. Update `Reading.to_dict` to omit `structures` when empty, matching the current `summary` omission pattern.
3. Update `Reading.from_dict` to default missing `structures` to empty, so existing serialized readings continue to load.
4. Keep every existing summary renderer intact.
5. For each tradition, build structures from the same intermediate data currently used to build summary text.
6. Make `summary` a rendering of the structures where practical, but do not require downstream consumers to use it.
7. Add focused round-trip tests for empty structures, one relation, one sequence, and one grid.
8. Add tradition-level replay tests asserting that structures are identical between initial cast and replay.

During migration, `Reading.summary` should remain the compatibility and CLI surface:

- Astrology continues to show `Aspects: ...`.
- Four Pillars continues to show element distribution, Day Master strength, Luck Pillars, and annual pillar.
- Nine Star Ki continues to show solar year/month/day/tendency and annual/monthly chart text.

The new structures should be additive and safe for consumers to ignore.

## Open Design Questions

- Should `structures` be a flat tuple on `Reading`, or grouped as `relations`, `sequences`, and `grids`? A flat tagged tuple is more extensible; grouped fields are easier for simple clients.
- Should relation groups be explicit, or is deterministic id prefixing enough for consumers to collect all astrology aspects?
- Should scalar derived facts like Four Pillars element distribution and Day Master strength be modeled now, or deferred until a general `MetricSet` or `Assessment` primitive exists?
- Should `GridCell.symbol_id` require the symbol to exist in the active reading deck, or can grids reference deck symbols outside the spread positions? Nine Star Ki can use the same deck, but future grids may need external symbol spaces.
- Should structures be stored in `Draw` for replay, or only in `Reading`? Keeping them out of `Draw` preserves `Draw` as minimal recorded inputs, but storing them in `Reading` means old serialized readings cannot gain structures unless replayed.

## Recommended First Slice

Implement the extension in the smallest useful order when TODO #47 becomes active:

1. Add `Relation`, `Sequence`, and `Grid` value objects plus optional `Reading.structures`.
2. Port astrology aspects first because they are already computed as typed `Aspect` objects before rendering.
3. Port Four Pillars luck pillars next because they are already represented as typed `LuckPillar` objects.
4. Port Nine Star Ki Lo Shu charts after that, replacing the current chart strings with structured `Grid` data while preserving the same string rendering for `summary`.

This sequence exercises all three primitive kinds while keeping each implementation close to existing code paths.
