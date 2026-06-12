# API Docs and Quality Gate

## Summary

The project has MkDocs and mkdocstrings API documentation plus a canonical local gate. The test matrix is available through Hatch for Python 3.12, 3.13, and 3.14.

## Key Facts

- Public API docstrings are populated for core, astronomy, and the four tradition packages.
- Runnable examples live in `docs/index.md` and `docs/api/traditions/*.md`.
- Tarot examples use `build_engine()` plus `read()`.
- Computed-tradition examples use `build_engine()` plus `cast()`.
- `mkdocs build --strict` passes.
- Hatch matrix scripts run tests and full gates across Python 3.12, 3.13, and 3.14.

## Details

The API documentation pass was documentation-only: no runtime behavior, signatures, serialization schema, or public behavior changed. It expanded top-level core summaries, value-object docstrings, engine contracts, RNG helpers, provenance, reading serialization, errors, shared astronomy, and tradition package surfaces.

Examples must satisfy actual validation. `ReadingRequest` examples need deck and spread ids, and `Querent` examples need `id` and `display_name`. Computed tradition examples should avoid `read()` and caller-provided randomness.

Material for MkDocs may print its upstream MkDocs 2.0 advisory unless `NO_MKDOCS_2_WARNING=true` is set. The local `.venv` also reported an INFO that Ruff or Black was not installed there for mkdocstrings signature formatting, but the strict build still exited successfully.

## Files

- `docs/index.md`: Main documentation landing page with examples.
- `docs/api/traditions/tarot.md`: Tarot API page and example.
- `docs/api/traditions/astrology.md`: Astrology API page and example.
- `docs/api/traditions/four_pillars.md`: Four Pillars API page and example.
- `docs/api/traditions/nine_star_ki.md`: Nine Star Ki API page and day-star escapement option.
- `mkdocs.yml`: MkDocs configuration.
- `pyproject.toml`: Dev dependencies and Hatch test matrix.
- `AGENTS.md`: Canonical commands and workflow rules.

## Test Coverage

Canonical local gate:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

Cross-version Hatch gate:

```bash
hatch run test:run
hatch run test:check
hatch run +py=3.14 test:run
```

Docs gate:

```bash
.venv/bin/python -m mkdocs build --strict
```

Known passing snapshots include ruff, mypy strict over 128 source files, and 90 tests on Python 3.12.11, 3.13.11, and 3.14.0 through `hatch run test:check`.

## Pitfalls

- Do not show computed traditions with caller randomness in examples.
- Keep doc changes aligned with actual validation requirements.
- The local MkDocs advisory text is external tool output, not a project warning when the strict build exits successfully.
