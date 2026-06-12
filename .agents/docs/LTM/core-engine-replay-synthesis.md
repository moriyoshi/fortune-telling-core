# Core Engine Replay Synthesis

## Summary

The core engine model supports both random-draw and computed traditions through the same primitives: symbols, spreads, selections, draws, structural readings, deterministic summaries, and provenance. `Draw` is the strongest replay artifact, while seed replay is useful but inherently narrower because it depends on compatible RNG and interpreter behavior. Discretionary interpretation and localization are intentionally outside core and can be supplied by the sibling interpreter package.

## Included Documents

| Document | Focus |
|----------|-------|
| [core-reading-model-and-replay.md](./core-reading-model-and-replay.md) | Core primitives, engine protocol, serialization, deterministic RNG, and replay guarantees. |
| [computed-tradition-pattern.md](./computed-tradition-pattern.md) | `cast()`/`NullRng` idiom, ephemeris-free replay, summary-only derived data, and provenance notes. |
| [tarot-reference.md](./tarot-reference.md) | Random-draw reference engine, RWS deck/spreads, and optional reversals. |
| [interpreter-package-boundary.md](./interpreter-package-boundary.md) | Boundary between structural core readings and the sibling interpretation/localization package. |

## Stable Knowledge

- The top-level public API exposes only tradition-neutral core types.
- The core never names tarot, astrology, BaZi, Nine Star Ki, signs, houses, stars, or other tradition-specific concepts.
- `Selection.modifiers` is the sanctioned place for per-selection state that the core does not interpret.
- `Draw` records the determined outcome and is the authoritative replay artifact.
- `Provenance.notes` records deterministic backend choices that do not warrant core schema fields.
- Random traditions use `read(request, rng=...)`; computed traditions should expose `cast()` and avoid caller randomness.
- `RandomRng` owns the Fisher-Yates shuffle contract; do not rely on `random.shuffle`.
- `SCHEMA_VERSION` is currently `1`, with hand-written serialization and explicit unknown-version errors.
- Discretionary interpretation, localization, and request question text are outside the library and belong in consuming harnesses.
- `Reading.summary`, when present, is deterministic structural output in plain American English.
- Core uses `pkgutil.extend_path` so a sibling distribution can contribute `fortune_telling_core.*` modules while core keeps API-bearing `__init__.py` files.
- Public `coerce` and `serde_types` helpers exist so namespace contributors do not depend on private core modules.

## Operational Guidance

When adding or changing a tradition, start by mapping its domain to `Deck`, `Spread`, and `Selection` without adding core fields. Put domain-specific facets in `Selection.modifiers` and record auditable choices in `Provenance.notes`.

Use `read()` for random-draw engines such as tarot. Use `cast()` with `NullRng` for deterministic computed engines and keep `provenance.rng_kind` and `provenance.rng_seed` as `None`.

Replay tests should prove that `replay(request, reading.draw)` equals the original reading. For computed traditions, replay must also work with an ephemeris that raises if called.

When integrating interpretation, apply it outside core over a structural `Reading`. Do not restore `PositionReading.interpretation`, `Provenance.interpretation_data_id`, `ReadingRequest.locale`, `ReadingRequest.question`, or engine interpretation hooks. Namespace contributors should import public helper modules such as `fortune_telling_core.coerce` and `fortune_telling_core.serde_types`, not private core modules.

## Files

- `src/fortune_telling_core/engine.py`: `Engine` protocol and `AbstractEngine` plumbing.
- `src/fortune_telling_core/draw.py`: `Selection` and `Draw`, the replay anchor.
- `src/fortune_telling_core/provenance.py`: Audit metadata and `notes`.
- `src/fortune_telling_core/serde.py`: Schema-versioned reading JSON.
- `src/fortune_telling_core/coerce.py`: Public coercion helpers for core and namespace contributors.
- `src/fortune_telling_core/serde_types.py`: Public serde helper types for core and namespace contributors.
- `src/fortune_telling_core/rng.py`: Random and sequence RNG behavior.
- `src/fortune_telling_core/_null_rng.py`: Shared sentinel for computed traditions.
- `src/fortune_telling_core/traditions/tarot/engine.py`: Random-draw reference engine.
- `src/fortune_telling_core/traditions/*/engine.py`: Tradition-specific engine implementations.
- `fortune_telling_core.interpretation`: Interpreter-owned module contributed by the sibling package.

## Tests

Core coverage should include value-object validation, serde round-trip, unknown schema handling, RNG determinism, and strict replay stubs. Tradition coverage should include deterministic replay for every engine.

Cross-package checks should import core `Reading` and interpreter-contributed modules in the same interpreter. Run each repository's gate from its own working directory with its own `./.venv`.

Run:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

## Pitfalls

- Do not add tradition concepts to the core schema when modifiers or provenance notes are enough.
- Do not conflate seed replay with recorded-draw replay.
- Do not show computed traditions with caller randomness in examples.
- Do not reintroduce interpretation hooks, locale selection, or question framing into the core engine contract.
- Do not make namespace contributors depend on private core modules.
- Recreate a virtualenv after renaming a package directory because editable-install records and console-script shebangs contain absolute paths.
- Summary-only outputs are not queryable structured data; a future relation, sequence, or grid model would be a deliberate core extension.
