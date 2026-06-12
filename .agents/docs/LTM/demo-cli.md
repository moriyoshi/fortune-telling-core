# Demo CLI

## Summary

The package includes a dependency-free `fortune-telling-demo` console script backed by `fortune_telling_core.cli`. It demonstrates the bundled tarot, astrology, Four Pillars, and Nine Star Ki engines through deterministic sample requests and exposes enough options to exercise replay-relevant inputs.

## Key Facts

- The console script is `fortune-telling-demo`.
- Text mode renders engine, deck or spread provenance, recorded draw size, position placements, summaries, and provenance notes.
- `--json` emits the serialized reading payload for one demo, or a list of serialized readings for `all`.
- User-settable inputs include tarot `--seed`, computed-tradition `--birth-datetime`, `--latitude`, `--longitude`, Four Pillars `--gender`, and `--target-year`.
- Naive `--birth-datetime` values are interpreted in the terminal or system local timezone and serialized back as aware ISO strings.

## Details

The CLI is a deterministic smoke-test and demonstration surface for the bundled engines. Tarot demos use seeded randomness. Computed-tradition demos pass explicit birth datetime and location inputs into `ReadingRequest`, then rely on each backend's `cast()` path rather than caller-supplied randomness.

Datetime parsing happens at the argument boundary. Invalid datetime strings fail with an argparse error. Offset-aware values are preserved. Naive values are interpreted as local terminal or system time through Python's local timezone handling before being sent to computed engines.

## Files

- `src/fortune_telling_core/cli.py`: Demo CLI implementation.
- `pyproject.toml`: Console-script entry point.
- `README.md`: Demo CLI examples and notes.
- `tests/test_cli.py`: CLI coverage.

## Test Coverage

Focused CLI validation has included:

```bash
python -m pytest tests/test_cli.py
python -m pytest
hatch run test:check
```

The full cross-version gate has passed across Python 3.12, 3.13, and 3.14 after the CLI additions.

## Pitfalls

- Keep computed-demo examples deterministic and avoid caller-provided randomness.
- Do not reintroduce locale flags to the demo CLI unless a harness-owned interpretation layer is added outside the core.
- Naive CLI datetimes are user-convenience input only; engine-facing requests should remain explicit and reproducible after parsing.
