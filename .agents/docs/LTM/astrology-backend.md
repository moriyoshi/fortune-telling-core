# Astrology Backend

## Summary

The astrology backend casts deterministic natal charts using an injected ephemeris and the shared core model. It supports tropical and sidereal zodiac modes, Whole Sign, Equal, and Placidus houses, ten planets plus lunar nodes, Ascendant and Midheaven, and aspects rendered into the reading summary.

## Key Facts

- Astrology lives under `src/fortune_telling_core/traditions/astrology/`.
- Consumers import astrology from the tradition subpackage, not from the top-level core.
- `AstrologyEngine.cast()` is the preferred public entrypoint.
- Replay recomputes aspects from recorded longitude modifiers, not from a fresh ephemeris call.
- `Provenance.notes` records ephemeris, house system, zodiac, and ayanamsa.
- The built-in Placidus implementation uses iterative semi-arc solving for intermediate cusps, with polar-circle failure semantics.

## Details

Astrology maps zodiac signs to a `Deck` and natal chart bodies/angles to a `Spread`. Each placement is a `Selection`: `position_id` is the body or angle, `symbol_id` is the sign, and `modifiers` carry house, degree, retrograde, longitude, and speed.

The supported chart scope includes Sun, Moon, Mercury through Pluto, north node, south node, Ascendant, and Midheaven. Sidereal mode applies an ayanamsa offset after tropical longitude calculation. Whole Sign and Equal houses are exact closed forms. Placidus derives RAMC from the geometric Midheaven, iterates intermediate cusps 11, 12, 2, and 3 from the Placidus semi-arc equations, and derives opposite cusps by opposition. It preserves high-latitude undefined behavior and can fall back when explicitly configured.

Aspects are computed from recorded longitudes over the major five aspects and rendered into `Reading.summary`. Discretionary sign, house, retrograde, or aspect meanings belong in the consuming harness.

Placidus tests use public geometric formulae and an independent bisection helper. They do not install, import, cite, or use `pyswisseph`, Swiss Ephemeris, AGPL/copyleft source, or any copyleft verification oracle.

## Files

- `src/fortune_telling_core/traditions/astrology/__init__.py`: Public tradition surface and `build_engine`.
- `src/fortune_telling_core/traditions/astrology/engine.py`: `AstrologyEngine`, `cast()`, provenance, and aspect summary rendering.
- `src/fortune_telling_core/traditions/astrology/birth.py`: Birth-data parsing.
- `src/fortune_telling_core/traditions/astrology/chart.py`: Chart casting.
- `src/fortune_telling_core/traditions/astrology/config.py`: Chart configuration.
- `src/fortune_telling_core/traditions/astrology/houses.py`: House calculations.
- `src/fortune_telling_core/traditions/astrology/aspects.py`: Aspect definitions and rendering.
- `tests/traditions/astrology/`: Regression tests.

## Test Coverage

- Zodiac and spread shape.
- Built-in and fixed ephemeris behavior.
- Determinism and replay without ephemeris calls.
- Core serde round-trip.
- Whole Sign, Equal, Placidus, and high-latitude handling.
- Numerical Placidus reference coverage using independent public formulae.
- Aspect orb behavior and node-opposition suppression.
- Sidereal deck behavior.
- Malformed birth input.
- No top-level core leakage.

## Pitfalls

- Use `cast()`, not `read()`, for honest `rng_kind` provenance.
- Aspects are summary-only, not structured queryable data.
- Placidus depends on true-obliquity geometry; sidereal chart output must keep using tropical geometry anchors before applying the zodiac offset.
- Do not use Swiss Ephemeris or `pyswisseph` as an implementation aid or verification oracle; the zero-copyleft policy applies to tests and scratch validation too.
- Keep discretionary astrology meanings outside the core library; harnesses can interpret signs, houses, retrograde modifiers, and aspect summaries.
