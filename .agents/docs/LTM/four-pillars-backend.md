# Four Pillars Backend

## Summary

The Four Pillars backend computes BaZi natal pillars, Ten Gods, element analysis, luck pillars, and annual pillars from birth data and solar-term boundaries. It reuses shared astronomy and the computed-tradition replay pattern without changing the core model.

## Key Facts

- Four Pillars lives under `src/fortune_telling_core/traditions/four_pillars/`.
- The deck contains 22 symbols: 10 Heavenly Stems and 12 Earthly Branches.
- The spread contains 8 positions: year, month, day, and hour stem/branch.
- Year boundary is Lichun/Risshun at Sun longitude 315 degrees.
- Month boundaries use the 12 sectional solar terms.
- Year epoch is `1984 = Jia-Zi`; day epoch is `1984-02-02 = Jia-Zi` through `DAY_JIAZI_JDN`.
- Time models are `CLOCK`, `LOCAL_MEAN_TIME`, and `TRUE_SOLAR`.
- Luck direction/start age and month-cycle index are stamped into day-stem modifiers for ephemeris-free replay.

## Details

The backend computes:

- Year pillar from the Lichun solar-year boundary.
- Month pillar from sectional solar-term boundaries and the Five Tigers rule.
- Day pillar from a continuous sexagenary count over the effective local date.
- Hour pillar from the hour branch and the Five Rats rule.
- Ten Gods relative to the Day Master.
- Element distribution and a documented Day Master strength heuristic.
- Luck pillars using direction and 3-days-per-year start-age convention.
- Annual pillar using `target_year` or `request.requested_at.year`.

`TimeModel` affects the local wall fields used for day and hour boundary decisions. The true UTC instant is still used for solar longitude. `DayBoundary.LATE_ZISHI` rolls the day forward when the effective local hour is 23.

Four Pillars originally introduced shared astronomy extraction from astrology. Later, its solar-term and time-model modules became compatibility shims over `fortune_telling_core.astronomy.solar_terms` and `fortune_telling_core.astronomy.time_model`.

## Files

- `src/fortune_telling_core/traditions/four_pillars/__init__.py`: Public tradition surface and `build_engine`.
- `src/fortune_telling_core/traditions/four_pillars/engine.py`: Engine, `cast()`, structural summary, and provenance.
- `src/fortune_telling_core/traditions/four_pillars/stems.py`: Heavenly stems.
- `src/fortune_telling_core/traditions/four_pillars/branches.py`: Earthly branches and hidden stems.
- `src/fortune_telling_core/traditions/four_pillars/cycle.py`: Sexagenary cycle helpers.
- `src/fortune_telling_core/traditions/four_pillars/pillars.py`: Pillar formulas.
- `src/fortune_telling_core/traditions/four_pillars/luck.py`: Luck pillars.
- `src/fortune_telling_core/traditions/four_pillars/ten_gods.py`: Ten Gods and element analysis.
- `src/fortune_telling_core/traditions/four_pillars/solar_terms.py`: Compatibility shim plus BaZi month branch helper.
- `src/fortune_telling_core/traditions/four_pillars/time_model.py`: Compatibility shim.
- `tests/traditions/four_pillars/`: Regression tests.

## Test Coverage

- Reference charts with `FixedEphemeris` pinned solar-term instants.
- Year and month boundary edges around Lichun and sectional terms.
- Hour boundaries and late-zi behavior.
- Day-pillar continuity and anchor.
- Five Tigers and Five Rats tables.
- Ten Gods table.
- Luck direction and start age.
- Annual pillar anchors such as 1984 Jia-Zi and 2024 Jia-Chen.
- Time-model switching.
- Cast/replay equality with a raising ephemeris.
- Serde round-trip and validation errors.
- No top-level core leakage.

## Pitfalls

- Solar-term accuracy near boundaries depends on ephemeris quality.
- Historical timezone rules are out of scope; caller supplies the civil offset in the timezone-aware datetime plus longitude.
- Luck pillars and annual pillars are summary-only.
- Gender input is used only for luck-direction convention and should stay neutrally modeled.
