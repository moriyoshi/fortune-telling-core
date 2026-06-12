# Architecture

The implementation architecture is a Python package with a deterministic tradition-agnostic core, optional tradition modules, and a shared astronomy subsystem for computed traditions.

## Current State

- `src/fortune_telling_core` contains the importable Python package.
- `src/fortune_telling_core/traditions` contains tradition-specific modules.
- `src/fortune_telling_core/astronomy` contains shared dependency-free astronomy.
- `src/fortune_telling_core/cli.py` provides the dependency-free `fortune-telling-demo` smoke-test and demonstration console script.
- `tests` contains the test suite.
- `docs` and `mkdocs.yml` contain the generated API documentation site.
- `tools/ephemeris` contains build-time sources and a generator for built-in ephemeris series.
- `pyproject.toml` declares package metadata, development tooling, and the Hatch Python-version matrix.
- `.agents/docs` contains project memory and agent-facing documentation.

## Core Model

The core package exposes tradition-neutral primitives only. Its central types are:

- `Symbol` and `Deck`: Opaque symbols and ordered or weighted symbol pools.
- `Position` and `Spread`: Reading slots and their order.
- `Selection` and `Draw`: Recorded outcomes and per-selection modifiers.
- `ReadingRequest`, `Reading`, `PositionReading`, and `Provenance`: Inputs, outputs, and audit metadata.
- `Engine` and `AbstractEngine`: The protocol and shared plumbing for `draw`, `interpret`, `read`, and `replay`.

`Selection.modifiers` is the main extension point for tradition-specific state. `Provenance.notes` records deterministic backend choices, school options, and implementation anchors that should be auditable without expanding the core schema.

Discretionary interpretation, localisation, and presentation copy are delegated to the consuming fortune-telling harness. The core emits stable structural readings plus deterministic `Reading.summary` renderings where no first-class relation, sequence, or grid model exists yet. When present, `Reading.summary` is always plain American English.

## Replay and Determinism

`Draw` is the authoritative replay artifact. Seed replay is supported for compatible library and interpreter behavior, but recorded-draw replay is the stronger guarantee because it does not depend on future RNG implementation details.

Random-draw traditions use `read(request, rng=...)`. Computed traditions expose `cast()` and use `NullRng` internally so `provenance.rng_kind` and `provenance.rng_seed` stay `None`. Computed replay must rebuild the reading from recorded `Selection.modifiers` without calling an ephemeris or any other external calculation source.

Serialization is hand-written and schema-versioned. `SCHEMA_VERSION` is currently `1`; unknown future versions raise `SchemaVersionError`, and additive fields are read with defaults where appropriate.

Core serializer support that namespace contributors need is public: use `fortune_telling_core.coerce` and `fortune_telling_core.serde_types` rather than private modules.

## Shared Astronomy

`fortune_telling_core.astronomy` is a sibling package to `traditions`, not a top-level public core export. It owns Julian-day helpers, Delta-T, nutation, ecliptic positions, solar longitude/crossing helpers, sectional solar terms, time-model adjustments, and ephemeris implementations.

`Ephemeris` mirrors the core `Rng` boundary: it is injectable, has deterministic built-in and fixed implementations, and gives traditions a clean precision seam. `BuiltinEphemeris.version` is `0.2.1` after exposing Moon ecliptic latitude from the existing Meeus latitude table. The runtime `builtin_series.py` is generated deterministically from public VSOP87D files downloaded into the ignored local cache under `.cache/ephemeris/vsop87d/` and structured Meeus tables by `tools/ephemeris/generate_builtin_series.py`, with checksum verification under `tools/ephemeris/sources/MANIFEST.sha256`.

Four Pillars and Nine Star Ki share solar-term and time-model code through `astronomy/solar_terms.py` and `astronomy/time_model.py`. Boundary-sensitive tests should pin crossings with `FixedEphemeris` rather than relying on default ephemeris precision.

## Tradition Modules

Traditions live under `fortune_telling_core.traditions.*` and are not re-exported from the top-level package.

- `tarot`: Random-draw reference using the 78-card Rider-Waite-Smith deck, single-card and three-card spreads, and optional reversals.
- `astrology`: Computed natal charts with tropical/sidereal zodiac modes, Whole Sign, Equal, and Placidus houses, bodies/angles, and aspects rendered into `Reading.summary`.
- `four_pillars`: Computed BaZi charts with stems, branches, year/month/day/hour pillars, Ten Gods, element analysis, luck pillars, annual pillars, time models, and day-boundary options.
- `nine_star_ki`: Computed principal, monthly, daily, and tendency stars plus annual/monthly Lo Shu charts, with configurable day-star escapement.

When established schools diverge, expose a focused option with a documented default and record the chosen value in `Provenance.notes`. Do not hardcode a disputed convention into shared primitives.

## Interpretation Boundary

The core library does not ship per-tradition interpretation datasets, locale negotiation, request question text, or human-facing meaning text. Harnesses own those concerns and can use structural fields such as `Selection.symbol_id`, `Selection.position_id`, modifiers, `Reading.summary`, and `Provenance.notes` as stable inputs.

The sibling `fortune-telling-core-interpreter` package provides the current package boundary for bundled interpretation and localization data. Core uses `pkgutil.extend_path` in package `__init__` files so sibling distributions can contribute `fortune_telling_core.*` modules while core keeps its API-bearing `__init__.py` files. Do not restore `PositionReading.interpretation`, `Provenance.interpretation_data_id`, `ReadingRequest.locale`, or engine interpretation hooks to core.

## Derived Outputs

The core currently has no first-class relation, sequence, or grid model. Tradition-specific derived structures such as astrology aspects, Four Pillars luck pillars, annual pillars, and Nine Star Ki Lo Shu charts are therefore rendered into `Reading.summary` and made reproducible by values stamped into `Selection.modifiers`. Summary text is a structural rendering and, when present, is always plain American English.

A future queryable relations, sequence, or grid API would be a deliberate core schema extension and should include serialization and replay design.

## Licensing and Dependencies

The package is MIT licensed, has no required runtime dependencies, and must remain zero-copyleft for commercial closed-source consumption. Swiss Ephemeris and `pyswisseph` are not shipped, even as optional extras. Consumers that need a licensed or higher-precision astronomy backend should provide their own `Ephemeris` implementation.

## Documentation and Quality

MkDocs and mkdocstrings render public API documentation from `docs` and package docstrings. Examples should use `read()` for tarot and `cast()` for computed traditions.

Code changes should preserve deterministic replay, type safety, and strict local quality gates. Cross-version behavior is covered by the Hatch matrix for Python 3.12, 3.13, and 3.14.

Public package artifacts should contain the importable package plus normal metadata such as `LICENSE`, `README.md`, and `pyproject.toml`. Local agent memory and tool compatibility scaffolding, including `.agents/` and `.claude/`, are excluded from distributions.
