# Core Reading Model and Replay

## Summary

The core model is tradition-agnostic and centers on symbols, positions, selections, draws, structural readings, deterministic summaries, provenance, and deterministic engines. A recorded `Draw` is the authoritative replay artifact, while seed reproducibility is supported for the same request, library version, and interpreter family. When present, `Reading.summary` is always plain American English.

## Key Facts

- The top-level public API exposes only tradition-neutral core types.
- Core dataclasses are frozen, slotted, manually serialized, and schema-versioned.
- The core never names tarot, astrology, BaZi, Nine Star Ki, signs, houses, or other tradition-specific concepts.
- `Selection.modifiers` is the extensibility point for per-selection state such as orientation, longitude, house, ten-god data, or star metadata.
- `Draw` embeds the determined outcome and is the replay authority.
- `Provenance.created_at` is derived from `ReadingRequest.requested_at` for value-equality reproducibility.
- `ReadingRequest` carries mechanical request metadata only; `question` was removed because it only framed discretionary interpretation.
- Core readings have no bundled interpretation fields, locale selection, interpretation dataset provenance, or engine interpretation hooks.
- Public `coerce` and `serde_types` helpers exist so namespace contributors do not depend on private core modules.

## Details

The core abstractions are:

- `Symbol` and `Deck`: Opaque symbols and ordered or weighted symbol pools.
- `Position` and `Spread`: Reading slots and their order.
- `Selection` and `Draw`: Determined choices for each position, plus modifiers.
- `Querent` and `ReadingRequest`: Mechanical request metadata, options, and typed timestamps.
- `PositionReading` and `Reading`: The final self-contained result.
- `Provenance`: Audit metadata for engine, deck, spread, randomness, and notes.
- `Engine` and `AbstractEngine`: The protocol and shared plumbing for draw, interpret, read, and replay.

The engine contract separates determined selection from structural reading construction:

- `draw(request, rng) -> Draw`: The only core-engine phase that may touch randomness.
- `interpret(request, draw) -> Reading`: Build a structural reading from a recorded draw.
- `read(request, *, rng) -> Reading`: Draw then build the reading.
- `replay(request, draw) -> Reading`: Validate the recorded draw and rebuild without RNG.

Discretionary interpretation, localization, and presentation copy are owned by the consuming harness, not by this core library.

The core used to carry locale and interpretation lookup machinery during early development, but that surface was removed before release. `PositionReading.interpretation`, `Provenance.interpretation_data_id`, `ReadingRequest.locale`, `ReadingRequest.question`, engine interpretation hooks, and per-tradition interpretation packages are intentionally absent. Consumers that need meanings or localization should apply a separate interpreter over the structural `Reading`.

`Reading.summary` is different from interpretation text: it is a deterministic structural rendering for derived outputs that do not yet have first-class relation, sequence, or grid types. Summary text is always plain American English when present.

Serialization is hand-written per dataclass. `SCHEMA_VERSION` is currently `1`; unknown future versions raise `SchemaVersionError`, and additive fields are tolerated through defaults. `reading_to_json` and `reading_from_json` round-trip a full reading. Mapping fields normalize to plain `dict`, so readings are intentionally non-hashable but have stable value equality.

## Files

- `src/fortune_telling_core/__init__.py`: Curated tradition-neutral public exports.
- `src/fortune_telling_core/rng.py`: `Rng`, `RandomRng`, and `SequenceRng`.
- `src/fortune_telling_core/symbols.py`: `Symbol` and `Deck`.
- `src/fortune_telling_core/spread.py`: `Position` and `Spread`.
- `src/fortune_telling_core/draw.py`: `Selection` and `Draw`.
- `src/fortune_telling_core/request.py`: `Querent` and `ReadingRequest`.
- `src/fortune_telling_core/reading.py`: Position readings and full readings.
- `src/fortune_telling_core/provenance.py`: Provenance metadata.
- `src/fortune_telling_core/engine.py`: Engine protocol and abstract engine.
- `src/fortune_telling_core/serde.py`: Schema-versioned JSON helpers.
- `src/fortune_telling_core/coerce.py`: Public coercion helpers for core and namespace contributors.
- `src/fortune_telling_core/serde_types.py`: Public serde helper types for core and namespace contributors.
- `src/fortune_telling_core/errors.py`: Shared error hierarchy.

## Test Coverage

- RNG determinism and strict sequence exhaustion.
- Deck, spread, and draw validation.
- Dataclass and JSON round-trips, including full `Reading` values.
- Unknown schema version handling and additive-field tolerance.
- Tradition replay tests prove `Draw` self-sufficiency.

Run:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

## Pitfalls

- Do not add tradition-specific fields to core primitives when `options`, `attributes`, `modifiers`, or `Provenance.notes` are sufficient.
- Do not reintroduce bundled interpretation, question text, or locale selection into the core; harnesses own that discretionary layer.
- Treat seed reproducibility and draw replay differently: seed replay is tied to compatible library and interpreter behavior, while recorded draw replay is the stronger guarantee.
- If a future feature needs queryable relations, grids, or sequences, that is a real core extension and should be designed explicitly.
