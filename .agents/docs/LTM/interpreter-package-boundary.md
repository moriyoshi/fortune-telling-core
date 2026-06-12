# Interpreter Package Boundary

## Summary

`fortune-telling-core` is a structural reading library. Discretionary interpretation, locale resolution, registries, and bundled meaning datasets live in the sibling `fortune-telling-core-interpreter` package, which contributes modules under the shared `fortune_telling_core` namespace.

## Key Facts

- Core emits deterministic structural readings, summaries, draws, modifiers, and provenance.
- Interpretation meanings, localization, and presentation copy are outside core.
- The sibling distribution is named `fortune-telling-core-interpreter`.
- The import namespace remains `fortune_telling_core`.
- Core uses `pkgutil.extend_path` in package `__init__` files so a sibling distribution can contribute `fortune_telling_core.*` submodules while core keeps API-bearing `__init__.py` files.
- Core serializer helpers were promoted from private `_coerce` and `_serde_types` modules to public `coerce` and `serde_types` modules for namespace contributors.
- Cross-import was verified with core `Reading`, interpreter `fortune_telling_core.interpretation`, `_locale`, and tarot interpretation dataset imports in one interpreter.

## Details

The integrated interpretation layer was removed from core before release. The removed core surface included `interpretation.py`, `_interpretation_registry.py`, `_locale.py`, `PositionReading.interpretation`, `Provenance.interpretation_data_id`, `ReadingRequest.locale`, interpretation-era engine hooks, and per-tradition interpretation packages.

The sibling interpreter applies standalone lookup over structural core readings:

```python
interpret(reading, dataset_or_registry, locale="en-GB")
```

This keeps mechanical fortune-telling behavior in core and discretionary meanings in an add-on package. The interpreter package was originally scaffolded as `fortune-telling-interpreter` and later renamed to `fortune-telling-core-interpreter`; the Python import namespace did not change.

Strict PEP 420 namespace packages were not used for core because they would force moving the top-level public API out of `fortune_telling_core/__init__.py`. `pkgutil.extend_path` lets core keep curated API exports while allowing sibling distributions to contribute submodules.

## Files

- `src/fortune_telling_core/__init__.py`: Core public API and namespace extension.
- `src/fortune_telling_core/coerce.py`: Public coercion helpers used by core and namespace contributors.
- `src/fortune_telling_core/serde_types.py`: Public serde helper types used by core and namespace contributors.
- `fortune-telling-core-interpreter`: Sibling package directory outside this repository.
- `fortune_telling_core.interpretation`: Interpreter-owned module contributed by the sibling package.

## Test Coverage

Core gate passed with 93 tests after the split. Interpreter gate passed with 19 tests. Cross-import was verified in the interpreter virtualenv by importing core `Reading`, interpreter modules, and the tarot interpretation dataset together.

Run each repository's gate from that repository's own working directory with that repository's own `./.venv`.

## Pitfalls

- Do not restore integrated interpretation fields, locale selection, or engine interpretation hooks to core.
- Do not make namespace contributors depend on private core modules; use public `coerce` and `serde_types`.
- Do not run one repository's virtualenv against another repository's working directory.
- Renaming a package directory breaks editable installs and console-script shebangs that contain absolute paths; recreate the virtualenv after such a rename.
- The interpreter sibling was not a git repository at the time of the split verification.
