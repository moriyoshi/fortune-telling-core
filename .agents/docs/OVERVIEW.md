# fortune-telling-core Project Overview

`fortune-telling-core` is a Python library for composable, reproducible fortune-telling and divination systems. It provides a small tradition-agnostic core plus tradition modules for tarot, astrology, Four Pillars, and Nine Star Ki.

## Scope

- Provide composable core primitives for reading requests, reading results, randomisable selections, spreads, symbols, structural summaries, and provenance.
- Support multiple traditions without forcing them into a single universal model.
- Keep deterministic execution possible through injectable random number generators, explicit draw inputs, or computed-tradition `cast()` entrypoints.
- Provide shared dependency-free astronomy for traditions that need celestial positions, solar terms, or time-model adjustments.
- Keep the package MIT licensed, zero-copyleft, and free of required runtime dependencies.
- Keep discretionary interpretation, localisation, and presentation copy outside core; the sibling `fortune-telling-core-interpreter` package can provide that layer over structural readings.
- Ship public artifacts as the importable package plus normal metadata, excluding local agent/tooling scaffolding such as `.agents/` and `.claude/`.
- Maintain project decisions, architecture notes, and agent-relevant findings in `.agents/docs/`.
- Maintain reusable long-term project memory under `.agents/docs/LTM/` as implementation knowledge accumulates.

## Major Subsystems

- Core reading model: Stable primitives for `Deck`, `Spread`, `Selection`, `Draw`, `Reading`, provenance, serialization, and engine contracts.
- Traditions: Tarot is the random-draw reference; astrology, Four Pillars, and Nine Star Ki are deterministic computed traditions.
- Shared astronomy: The `astronomy` package provides Julian-day helpers, Delta-T, nutation, solar crossings, solar terms, time models, and an injectable `Ephemeris` protocol with dependency-free built-in and fixed implementations.
- Demo CLI: `fortune-telling-demo` is a dependency-free smoke-test and demonstration surface for deterministic sample readings.
- Documentation and quality: MkDocs/mkdocstrings render public API docs, and Hatch runs the Python 3.12, 3.13, and 3.14 quality matrix.

## Boundaries

- The package stack is Python 3.12+ using a `src/` layout.
- No runtime web service, model provider, database, or UI framework is part of the library architecture. The packaged CLI is a demonstration and smoke-test surface, not an application framework.
- Cultural and symbolic systems should be represented explicitly rather than hard-coded into shared primitives.
- The top-level package exports tradition-neutral core types only; tradition-specific modules are imported from `fortune_telling_core.traditions.*`.
- Computed traditions render some derived structures, such as aspects, luck pillars, and Lo Shu charts, into `Reading.summary` because the core has no first-class relation, sequence, or grid model yet.
- Discretionary interpretation, localisation, and presentation copy are harness responsibilities, not core-library responsibilities. `fortune-telling-core-interpreter` is the sibling package boundary for bundled interpretation data.
- Higher-precision astronomy is a bring-your-own integration through the `Ephemeris` protocol; copyleft adapters such as Swiss Ephemeris are not shipped.

## Documentation Map

- `README.md`: human-facing project entrypoint.
- `AGENTS.md`: operating rules for coding agents.
- `.agents/docs/ARCHITECTURE.md`: current technical design.
- `.agents/docs/JOURNAL.md`: unconsolidated work history when present plus the canonical LTM consolidation record.
- `.agents/docs/LTM/INDEX.md`: durable long-term memory.
- `.agents/docs/TODO.md`: open backlog.
