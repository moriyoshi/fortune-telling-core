# Computed Tradition Pattern

## Summary

Astrology, Four Pillars, and Nine Star Ki are deterministic computed traditions rather than random draws. They share an engine idiom: use `cast()` with `NullRng`, keep randomness absent from provenance, stamp enough computed state into `Selection.modifiers`, and rebuild replay from the recorded `Draw` without ephemeris calls.

## Key Facts

- Computed engines still satisfy the core `Engine` protocol.
- Public callers should use `cast()` instead of `read()` for computed traditions.
- `draw()` accepts an `Rng` for protocol compatibility but should not consume it.
- `NullRng` raises `ExhaustedRngError` if any random method is touched.
- `provenance.rng_kind` and `provenance.rng_seed` remain `None`.
- Derived outputs that do not fit core positions are rendered into `Reading.summary`.
- Replay must be ephemeris-free and derived only from recorded selection modifiers.

## Details

The computed-tradition idiom emerged across three backends:

- Astrology computes placements, houses, and aspects from birth data and an injected ephemeris.
- Four Pillars computes stems, branches, Ten Gods, luck pillars, and annual pillars from birth data, solar terms, and calendrical formulas.
- Nine Star Ki computes principal, monthly, daily, and tendency stars plus annual/monthly Lo Shu charts from birth data and solar-term boundaries.

These backends map deterministic computation onto the same core primitives by making each computed result a `Selection`. Extra facets such as longitude, house, retrograde flag, hidden stems, ten-god relationships, star numbers, daily direction, and chart centers are stored in `Selection.modifiers`.

The `_interpret` override is the composition point. A backend can call `super()._interpret(...)` for ordinary validation and position resolution, then render deterministic summary content.

`Provenance.notes` records deterministic choices such as ephemeris id and version, time model, house system, zodiac, ayanamsa, solar-term basis, day-boundary rules, day-star escapement, and anchors.

## Files

- `src/fortune_telling_core/_null_rng.py`: Shared `NullRng`.
- `src/fortune_telling_core/_parsing.py`: Shared request parsing helpers for computed traditions.
- `src/fortune_telling_core/traditions/astrology/engine.py`: Astrology computed engine.
- `src/fortune_telling_core/traditions/four_pillars/engine.py`: Four Pillars computed engine.
- `src/fortune_telling_core/traditions/nine_star_ki/engine.py`: Nine Star Ki computed engine.
- `src/fortune_telling_core/astronomy/ephemeris/protocol.py`: Shared ephemeris injection boundary.

## Test Coverage

Each computed backend has tests for:

- `cast()` determinism.
- `replay(request, reading.draw)` equality.
- replay with an ephemeris that raises if called.
- `rng_kind is None`.
- serde round-trip of the full computed reading.
- no top-level core leakage from tradition modules.

## Pitfalls

- Do not call the ephemeris in `interpret()` or replay paths.
- Do not use `read()` in examples for computed traditions; it suggests randomness where none is needed.
- Summary-only outputs are not queryable structured data. A future first-class core `relations`, `sequences`, or grid model would require a deliberate schema change.
- When schools diverge, expose a documented option and record the selected value in `Provenance.notes`.
- Do not add supplemental interpretation datasets to computed engines; harnesses own discretionary meanings and localization.
