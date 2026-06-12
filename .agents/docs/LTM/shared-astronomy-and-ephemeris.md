# Shared Astronomy and Ephemeris

## Summary

The shared `astronomy` package provides deterministic, dependency-free astronomy for computed traditions. It owns Julian-day helpers, Delta-T, nutation, ecliptic positions, ephemeris protocols and implementations, solar crossings, solar terms, and time-model calculations.

## Key Facts

- `astronomy` is a sibling package to `traditions`, not part of the top-level core exports.
- `Ephemeris` mirrors the `Rng` pattern with an injectable protocol, deterministic default, and fixed test stub.
- `EclipticPosition.latitude` is optional; `BuiltinEphemeris` currently populates it for the Moon only.
- `BuiltinEphemeris.version` is `0.2.1` after exposing Moon ecliptic latitude from the existing Meeus latitude table.
- `builtin_series.py` is generated deterministically from checksum-verified public source data and checked Meeus tables.
- No Swiss Ephemeris adapter or `pyswisseph` extra is shipped.
- Solar-term code is shared by Four Pillars and Nine Star Ki.
- Time models are shared as `TimeModel.CLOCK`, `TimeModel.LOCAL_MEAN_TIME`, and `TimeModel.TRUE_SOLAR`.

## Details

The first extraction moved tradition-neutral astrology astronomy into `src/fortune_telling_core/astronomy/`. Compatibility shims remained under `traditions/astrology` so existing imports and tests continued to pass. Later, Four Pillars solar-term and time-model code moved into the same shared package so Nine Star Ki could use it without importing Four Pillars.

The Tier-1 ephemeris replaced an earlier single-sine Tier-0 model. It remains pure Python and dependency-free:

- Sun: Meeus-style apparent longitude with equation-of-center terms through `sin(3M)`, nutation, and aberration.
- Mercury through Neptune: truncated VSOP87D heliocentric tables from public IMCCE/Bureau des Longitudes data, geocentric reduction, one light-time iteration, FK5 correction, aberration, and nutation.
- Pluto: Meeus chapter 37 periodic heliocentric series with the same apparent-longitude path.
- Moon: Meeus chapter 47 abridged ELP-2000/82 longitude and latitude series with eccentricity factors and additive terms.
- Nodes: Meeus true-node polynomial/correction, with south node derived by 180 degrees.

Solar helpers include `sun_longitude`, `solar_longitude_crossing`, and `equation_of_time`. Solar-term helpers include `JIE_LONGITUDES`, `solar_month_index`, `adjacent_jie_crossing`, `lichun_crossing`, and `solar_term_crossing`.

The Tier-1 runtime series are reproducible from build-time sources. Public IMCCE/Bureau des Longitudes VSOP87D source files are not version-managed; they are downloaded on demand into the ignored local cache at `.cache/ephemeris/vsop87d/` with SHA-256 checksums in `tools/ephemeris/sources/MANIFEST.sha256`. Meeus Moon and Pluto periodic tables are structured in `tools/ephemeris/sources/meeus_tables.py`. The generator at `tools/ephemeris/generate_builtin_series.py` can populate missing VSOP87D files with `--download-missing`, verifies checksums, parses VSOP87D, keeps terms with `abs(A) >= 1e-7`, appends the Meeus tables, and writes `src/fortune_telling_core/astronomy/ephemeris/builtin_series.py`.

Normal tests stay offline by default. The generated-series reproducibility test skips when the VSOP87D cache is absent, but verifies source reproducibility when the cache is present.

`EclipticPosition(longitude, speed)` remains backwards-compatible because optional `latitude` follows the original positional fields. `None` means the backend or body does not provide ecliptic latitude. `BuiltinEphemeris` imports `MOON_LATITUDE_TERMS` from the generated series and populates latitude for `Body.MOON`; other bodies continue to report `None` until a backend explicitly computes latitude.

## Files

- `src/fortune_telling_core/astronomy/__init__.py`: Shared astronomy exports.
- `src/fortune_telling_core/astronomy/bodies.py`: Celestial body enum.
- `src/fortune_telling_core/astronomy/position.py`: `EclipticPosition` and degree normalization. `latitude` is optional and populated by `BuiltinEphemeris` for the Moon.
- `src/fortune_telling_core/astronomy/julian.py`: Julian day helpers.
- `src/fortune_telling_core/astronomy/deltat.py`: Delta-T approximation.
- `src/fortune_telling_core/astronomy/nutation.py`: Nutation and obliquity helpers.
- `src/fortune_telling_core/astronomy/solar.py`: Solar longitude, crossings, and equation of time.
- `src/fortune_telling_core/astronomy/solar_terms.py`: Shared sectional solar terms.
- `src/fortune_telling_core/astronomy/time_model.py`: Shared effective datetime calculation.
- `src/fortune_telling_core/astronomy/ephemeris/`: Protocol, built-in ephemeris, fixed ephemeris, and series data.
- `tests/astronomy/`: Shared astronomy tests.
- `tools/ephemeris/generate_builtin_series.py`: Deterministic generator for `builtin_series.py`.
- `tools/ephemeris/download_vsop87d.py`: Checksum-verified downloader for the local VSOP87D cache.
- `.cache/ephemeris/vsop87d/`: Ignored local cache for public VSOP87D source files.
- `.gitignore`: Ignores the project-local `.cache/` directory.
- `tools/ephemeris/sources/MANIFEST.sha256`: Checksums verified by the generator.
- `tools/ephemeris/sources/meeus_tables.py`: Structured Moon and Pluto tables transcribed from Meeus.

## Test Coverage

- Julian day examples and J2000.
- Delta-T continuity.
- Solar crossing mechanics, including 359-to-0 wrapping and unbracketed failures.
- Equation of time bounds.
- Shared solar-term and time-model tests.
- Builtin ephemeris accuracy vectors against checked-in Meeus worked examples.
- Moon latitude coverage near the Meeus chapter 47 worked example.
- Non-Moon bodies keep `latitude is None` under the built-in ephemeris.
- Builtin series generation check via `tests/astronomy/test_builtin_series_generation.py`.
- Tradition replay tests that prove recorded draws do not need fresh ephemeris calls.

Run the full gate after astronomy changes:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

For cross-version behavior, run:

```bash
hatch run test:check
```

To verify generated ephemeris series directly, run:

```bash
python tools/ephemeris/generate_builtin_series.py --check
python -m pytest tests/astronomy/test_builtin_series_generation.py tests/astronomy/test_builtin_ephemeris_accuracy.py tests/traditions/astrology/test_ephemeris.py
```

## Pitfalls

- Boundary-sensitive charts can flip near sign cusps, house cusps, Risshun, or sectional terms.
- Bump `BuiltinEphemeris.version` whenever series truncation or algorithms change, because provenance reproducibility depends on id plus version.
- Populate the local VSOP87D cache with `python tools/ephemeris/download_vsop87d.py`, then keep `builtin_series.py` in sync by running the generator in `--check` mode after source or threshold changes.
- Use `python tools/ephemeris/generate_builtin_series.py --download-missing` when regeneration should populate the local VSOP87D cache automatically.
- Keep copyleft astronomy libraries out of the package surface.
- `FixedEphemeris` is the right tool for pinning boundary tests independent of default ephemeris accuracy.
