# Licensing and Dependency Policy

## Summary

`fortune-telling-core` is MIT-licensed, zero-copyleft, and has no required runtime dependencies. The Swiss Ephemeris adapter and `pyswisseph` extra were removed because AGPL exposure is unacceptable for the commercial closed-source consumer.

## Key Facts

- The package ships under MIT.
- Required runtime dependencies remain empty.
- Copyleft dependencies and adapters should not be shipped in the library surface.
- `pyswisseph` and Swiss Ephemeris are dual-licensed AGPL-3.0 or paid commercial license, so the optional extra was removed.
- Higher-precision astronomy remains possible through the injectable `Ephemeris` protocol, but consumers own the licensing of their chosen backend.
- Shipped tarot text cites Waite's public-domain `The Pictorial Key to the Tarot`.
- Shipped astronomy code is original implementation of published methods and public coefficient data.

## Details

The project is intended for a commercial closed-source product, so even optional AGPL-referencing surfaces are inappropriate. The cleanup removed `src/fortune_telling_core/astronomy/ephemeris/swisseph.py`, the astrology re-export shim, and the `swisseph` optional dependency block from `pyproject.toml`.

The self-built `BuiltinEphemeris` keeps the package MIT-clean and dependency-free. VSOP87, ELP2000, JPL DE concepts, and Meeus methods are public-domain or freely distributable as data and algorithms; the problematic copyleft exposure was Swiss Ephemeris code, not celestial mechanics in general.

## Files

- `LICENSE`: MIT license text.
- `README.md`: Licensing and bring-your-own-ephemeris note.
- `pyproject.toml`: Empty runtime dependencies and no `swisseph` extra.
- `src/fortune_telling_core/astronomy/ephemeris/`: Pure-Python built-in and fixed ephemerides.
- `src/fortune_telling_core/astronomy/ephemeris/builtin_series.py`: Public coefficient tables and provenance comments.

## Test Coverage

Licensing policy is not directly testable, but dependency posture can be reviewed in `pyproject.toml`. Normal verification after policy-related removals was:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

## Pitfalls

- Do not reintroduce a Swiss Ephemeris adapter or extra without an explicit licensing decision.
- Optional dependencies can still create compliance audit risk.
- Bring-your-own ephemeris is the intended high-precision extension path.
