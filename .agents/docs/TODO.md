# Project To-Dos

Items extracted from planning, implementation work, and memory consolidation. Resolve or remove items once addressed.

## Implementation handoff

Nine Star Ki backend plus a shared solar-term/time-model extraction, recorded in `JOURNAL.md` under
"2026-06-12 - Design for a Nine Star Ki backend and shared solar-term/time-model extraction". Two
phases, no core changes. Single-writer (repo is not git) - Phase 1 must land green before Phase 2.

Phase 1 - extract shared, keep Four Pillars green:

1. New `astronomy/solar_terms.py` (move from `four_pillars/solar_terms.py`; `solar_month_index`
   replaces `months_since_yin`; `month_branch_index` stays BaZi-local) and `astronomy/time_model.py`
   (move `TimeModel` + `effective_datetime`). Export from `astronomy/__init__.py`.
2. New `_null_rng.py` (`NullRng`) and `_parsing.py` (require_string/parse_float/parse_latitude/
   parse_longitude/collect_values).
3. Update `four_pillars/{config,time_model,solar_terms}.py` to re-export from the shared locations so
   existing tests pass unchanged. Add `tests/astronomy/test_solar_terms.py` + `test_time_model.py`.

Phase 2 - `traditions/nine_star_ki/`:

4. `stars.py` (9 stars + Lo Shu data), `lo_shu.py` (`fly_chart`), `star_calc.py` (year/month/day/
   tendency), `birth.py`, `deck.py`, `spreads.py` (principal/monthly/daily/tendency), `chart.py`,
   `engine.py` (`NineStarKiEngine` + `cast()` + `build_engine`). Charts + tendency render into `summary`; replay stays ephemeris-free via stamped
   modifiers. Nothing added to the top-level `__init__`.
5. Tests under `tests/traditions/nine_star_ki/` per the journal's verification matrix; then the local
   gate (`ruff format`, `ruff check`, `mypy src tests`, `pytest`). Append your own `JOURNAL.md` entry
   recording the extraction and the Nine Star Ki anchor/escapement decisions. Do not commit unless asked.

## Open Items

- [x] Bootstrap the coding-agent-ready project structure.
- [x] Choose the initial library stack and record setup, build, lint, and test commands in `README.md` and `AGENTS.md`.
- [x] Define the first public API for readings, engines, symbols, spreads, structural summaries, and provenance. (Designed; see `JOURNAL.md` 2026-06-12; interpretation data later removed from core.)
- [x] Decide the initial supported fortune-telling tradition modules. (Tarot reference: RWS deck, single-card and three-card spreads.)
- [x] Implement the core data model per the agreed design.
- [x] Add focused tests for deterministic reading generation and serialization.
- [x] Implement the tarot reference engine with integer deck weights.
- [x] Implement the astrology backend per the agreed design (see `JOURNAL.md` 2026-06-12 astrology entry).
- [x] Extract the shared `astronomy` package and implement the Four Pillars (BaZi) backend (see `JOURNAL.md` 2026-06-12 Four Pillars entry).
- [x] Remove the AGPL pyswisseph extra/adapter, add the MIT `LICENSE` file, and document the zero-copyleft posture (see `JOURNAL.md` 2026-06-12 licensing entry).
- [x] Upgrade `BuiltinEphemeris` to Tier-1 accuracy (Sun, then VSOP87 planets, then ELP Moon) per the `JOURNAL.md` 2026-06-12 Tier-1 ephemeris design entry.
- [x] Extract shared solar-term/time-model code into `astronomy`, then implement the Nine Star Ki backend (see `JOURNAL.md` 2026-06-12 Nine Star Ki entry).
- [x] #46 Improve interpretation datasets across traditions beyond minimal/reference text. Resolved by removal: interpretation is delegated to the consuming harness. - *source: 2026-06-12 - Work summary and cross-cutting findings*
- [x] Consider a future first-class core `relations`, grid, or sequence extension for aspects, luck pillars, and Lo Shu charts. Design proposal written: see `.agents/docs/design/relations-grid-sequence-extension.md` (proposal only, not yet implemented). - *source: 2026-06-12 - Work summary and cross-cutting findings*
- [x] #48 Add additional locale datasets as additive interpretation data. Resolved by removal: locale datasets were removed with bundled interpretation. - *source: 2026-06-12 - Work summary and cross-cutting findings*
- [x] Consider replacing the low-precision Placidus quadrant interpolation with full semi-arc iteration. - *source: 2026-06-12 - Astrology backend implemented*
- [x] Consider exposing Moon latitude in the public astronomy model; the latitude table is checked in but `EclipticPosition` currently records longitude and speed only. - *source: 2026-06-12 - Tier-1 BuiltinEphemeris implemented*
- [x] #51 Add complete locale dataset shells for the target locales. Resolved by removal: the core no longer ships locale dataset shells. - *source: 2026-06-12 - Locale expansion plan*
- [x] #52 Improve terminology and translation quality per tradition, especially for Japanese, Chinese, and Korean esoteric terms. Resolved by removal: translation quality is a harness concern. - *source: 2026-06-12 - Locale expansion plan*
- [x] #53 Document supported locales, aliases, and fallback rules in the public docs. Resolved by removal: public locale docs were removed because locale selection is no longer in core. - *source: 2026-06-12 - Locale expansion plan*
- [x] Decide whether `.agents/` and `.claude/` should remain in the sdist before a public PyPI upload. - *source: 2026-06-12 - Publish readiness review and dependency-floor follow-up*
- [x] Run or add `twine check` before release. - *source: 2026-06-12 - Publish readiness review and dependency-floor follow-up*
- [x] Register the PyPI Trusted Publisher for owner `moriyoshi`, repository `fortune-telling-core`, workflow `cd.yml`, and environment `pypi`. Done manually in the GitHub UI by the owner. - *source: 2026-06-12 - GitHub Actions CI/CD and docs publishing workflows added*
- [x] Set repository Settings -> Pages -> Source to GitHub Actions. Done manually in the GitHub UI by the owner. - *source: 2026-06-12 - GitHub Actions CI/CD and docs publishing workflows added*
