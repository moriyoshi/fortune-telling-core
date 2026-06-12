# Nine Star Ki Backend

## Summary

The Nine Star Ki backend computes principal, monthly, daily, and tendency stars plus annual and monthly Lo Shu flying-star charts. It builds on shared solar-term and time-model helpers and exposes the divergent day-star escapement school as a configurable option.

## Key Facts

- Nine Star Ki lives under `src/fortune_telling_core/traditions/nine_star_ki/`.
- The deck has 9 star symbols with number, CJK name, color, five-element, trigram, and home-palace attributes.
- The spread has 4 positions: principal, monthly, daily, and tendency.
- Principal/year star uses Risshun at Sun longitude 315 degrees.
- Year anchor is `1900 -> 1 White`, decrementing one star per solar year.
- Monthly star uses year-star groups `{1,4,7}`, `{2,5,8}`, `{3,6,9}` with sector-0 starts `8`, `2`, and `5`.
- Tendency star is the home star of the palace occupied by the monthly star in the natal year chart; center case returns the principal star.
- Day-star escapement is configurable with `DayStarEscapement`.

## Details

Lo Shu data is explicit. Palace keys are `N`, `NE`, `E`, `SE`, `C`, `SW`, `W`, `NW`, and `S`. `fly_chart(center)` flies the fixed order `C,NW,W,NE,S,N,SW,E,SE`; `fly_chart(5)` equals the base Lo Shu chart, and the base chart sums to 15 per row, column, and diagonal.

Daily stars use solstice escapement. The default is `jiazi_at_or_before_solstice`, which anchors Star 1 or Star 9 to the Jia-Zi day at or before the active solstice. The alternate `first_jiazi_after_solstice` matches the documented Daily Flying Star convention that anchors to the first Jia-Zi day after the solstice. The selected value is stamped into draw modifiers and recorded in `Provenance.notes`.

Selections stamp star numbers, solar year, target year, solar month index, daily direction, tendency result, center-case flag, and rendered annual/monthly chart data so replay does not require an ephemeris.

## Files

- `src/fortune_telling_core/traditions/nine_star_ki/__init__.py`: Public tradition surface and `build_engine`.
- `src/fortune_telling_core/traditions/nine_star_ki/config.py`: `DayStarEscapement` and config.
- `src/fortune_telling_core/traditions/nine_star_ki/engine.py`: Engine, `cast()`, summary rendering, and provenance.
- `src/fortune_telling_core/traditions/nine_star_ki/stars.py`: Star metadata.
- `src/fortune_telling_core/traditions/nine_star_ki/lo_shu.py`: Lo Shu base data and `fly_chart`.
- `src/fortune_telling_core/traditions/nine_star_ki/star_calc.py`: Star formulas.
- `src/fortune_telling_core/traditions/nine_star_ki/birth.py`: Birth-data parsing.
- `src/fortune_telling_core/traditions/nine_star_ki/chart.py`: Chart-to-draw conversion.
- `docs/api/traditions/nine_star_ki.md`: API docs including day-star escapement option.
- `tests/traditions/nine_star_ki/`: Regression tests.

## Test Coverage

- Star-data integrity and Lo Shu magic-square sums.
- `fly_chart(5) == LO_SHU_BASE`.
- Year anchors and digit-sum oracles.
- Monthly-star group tables.
- Fixed-Sun day-direction pins.
- Tendency and center-case derivation.
- Risshun and sectional-term boundaries with `FixedEphemeris`.
- Cast/replay with a raising ephemeris.
- Serde round-trip and validation errors.
- Target-year annual chart behavior.
- Day-star escapement divergence on 2024-01-10.
- Request override records the selected escapement in provenance.
- No top-level core leakage.

## Pitfalls

- Day-star escapement is a genuine school divergence; do not hardcode a single convention.
- Lo Shu charts are summary-only.
- Risshun and sectional-term boundary accuracy depends on ephemeris quality.
- Keep discretionary Nine Star Ki meanings outside the core library; harnesses can interpret star ids, positions, and Lo Shu summaries.
