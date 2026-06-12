# Computed Traditions Astronomy Synthesis

## Summary

Astrology, Four Pillars, and Nine Star Ki share a deterministic computed-tradition architecture built on the shared `astronomy` package. They use `cast()`, `NullRng`, ephemeris-free replay, solar-term/time-model helpers where needed, and summary rendering for derived content that has no first-class core slot. Astronomy precision work stays dependency-free and zero-copyleft, including test oracles and scratch validation.

## Included Documents

| Document | Focus |
|----------|-------|
| [computed-tradition-pattern.md](./computed-tradition-pattern.md) | Shared engine idiom for deterministic traditions. |
| [shared-astronomy-and-ephemeris.md](./shared-astronomy-and-ephemeris.md) | Shared astronomy package, ephemeris protocol, solar helpers, time models, and accuracy boundaries. |
| [astrology-backend.md](./astrology-backend.md) | Natal chart placements, houses, aspects, and astrology replay behavior. |
| [four-pillars-backend.md](./four-pillars-backend.md) | BaZi pillars, Ten Gods, luck pillars, solar terms, and time models. |
| [nine-star-ki-backend.md](./nine-star-ki-backend.md) | Nine Star Ki stars, Lo Shu charts, solar-term boundaries, and day-star escapement options. |

## Stable Knowledge

- `astronomy` is a shared sibling package to `traditions`, not part of top-level core exports.
- `Ephemeris` is injectable and mirrors the core `Rng` boundary pattern.
- `EclipticPosition.latitude` is optional; `BuiltinEphemeris` currently populates it for `Body.MOON` only.
- `BuiltinEphemeris.version` is `0.2.1` after exposing Moon ecliptic latitude from the existing Meeus latitude table.
- `builtin_series.py` is a generated runtime artifact with deterministic source verification under `tools/ephemeris/`.
- `FixedEphemeris` is the correct tool for deterministic boundary tests.
- Four Pillars and Nine Star Ki share solar terms through `astronomy/solar_terms.py`.
- Four Pillars and Nine Star Ki share effective datetime handling through `astronomy/time_model.py`.
- Computed engine replay must reconstruct readings from recorded `Selection.modifiers` without fresh ephemeris calls.
- Astrology aspects, BaZi luck/annual pillars, and Nine Star Ki Lo Shu charts are summary-only.
- Placidus houses use iterative semi-arc solving from public geometric formulae and preserve high-latitude failure/fallback behavior.
- Genuine school divergences should be configurable and recorded in `Provenance.notes`.

## Operational Guidance

When touching computed backends, first decide whether the change is tradition-specific, shared astronomy, or shared computed-engine plumbing. Put reusable solar, ephemeris, and time-model behavior under `src/fortune_telling_core/astronomy/`; keep formulas that belong to one tradition under that tradition package.

Boundary-sensitive tests should use `FixedEphemeris` to pin crossings. Use the default `BuiltinEphemeris` for smoke and accuracy coverage, not for tests whose intent is a precise tradition boundary.

For replay, stamp all values needed to rebuild derived outputs into modifiers. Do not call the ephemeris from `_interpret` or replay. Add a raising-ephemeris regression test whenever new derived content is introduced.

For astrology house work, keep sidereal output anchored to tropical geometry before applying the zodiac offset. Placidus reference tests should use independent public formulae, not Swiss Ephemeris or `pyswisseph`.

## Files

- `src/fortune_telling_core/astronomy/`: Shared astronomy package.
- `src/fortune_telling_core/astronomy/ephemeris/`: Protocol, built-in ephemeris, fixed ephemeris, and series data.
- `tools/ephemeris/generate_builtin_series.py`: Verifies source checksums and regenerates `builtin_series.py`.
- `tools/ephemeris/download_vsop87d.py`: Populates the ignored local VSOP87D source cache under `.cache/`.
- `tools/ephemeris/sources/`: VSOP87D checksum manifest and structured Meeus tables.
- `src/fortune_telling_core/astronomy/solar.py`: Solar longitude, crossings, and equation of time.
- `src/fortune_telling_core/astronomy/solar_terms.py`: Shared sectional solar terms and Risshun/Lichun crossing helpers.
- `src/fortune_telling_core/astronomy/time_model.py`: Shared time-model adjustment.
- `src/fortune_telling_core/traditions/astrology/`: Astrology backend.
- `src/fortune_telling_core/traditions/four_pillars/`: Four Pillars backend.
- `src/fortune_telling_core/traditions/nine_star_ki/`: Nine Star Ki backend.
- `tests/astronomy/`: Shared astronomy tests.
- `tests/traditions/astrology/`, `tests/traditions/four_pillars/`, `tests/traditions/nine_star_ki/`: Computed backend tests.

## Tests

Run the local gate for normal changes:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

Run the Hatch matrix before reporting cross-version behavior as done:

```bash
hatch run test:check
```

Important regression categories:

- ephemeris accuracy vectors and solar crossing wrap behavior.
- Moon latitude coverage near the Meeus chapter 47 worked example, with non-Moon bodies keeping `latitude is None`.
- numerical Placidus reference coverage using independent public formulae.
- generated ephemeris series check with `python tools/ephemeris/generate_builtin_series.py --check` after populating the VSOP87D cache.
- cast/replay equality with `rng_kind is None`.
- replay with an ephemeris that raises if called.
- serde round-trip of full computed readings.
- boundary tests around Risshun/Lichun, sectional terms, house cusps, and solstice escapement.
- no top-level core leakage from tradition modules.

## Pitfalls

- Births close to solar terms, sign cusps, or house cusps are accuracy-sensitive.
- Bump `BuiltinEphemeris.version` when ephemeris algorithms or series change.
- Regenerate or check `builtin_series.py` when VSOP87D sources, Meeus tables, or the retained-term threshold change.
- Do not use Swiss Ephemeris, `pyswisseph`, or other copyleft code as a verification oracle.
- Do not reintroduce tradition-to-tradition imports for shared solar or time-model code.
- Do not hardcode divergent school choices such as Nine Star Ki day-star escapement.
- Keep discretionary interpretation and localization outside the core library; harnesses own that layer.
