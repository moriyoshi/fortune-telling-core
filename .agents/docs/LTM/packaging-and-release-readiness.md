# Packaging and Release Readiness

## Summary

The package is shaped for a pre-alpha publication with no required runtime dependencies. Build, dev, release, and docs dependency floors are refreshed, release artifacts have been smoke-tested, package versions are derived from git tags through hatch-vcs, and local agent scaffolding is excluded from public artifacts.

## Key Facts

- The source tree is publishable for `Development Status :: 2 - Pre-Alpha`.
- The runtime package intentionally declares no required dependencies.
- Dependency declarations use lower bounds rather than exact pins because they are package extras and build-system requirements, not an application lock file.
- `hatchling` has a floor of `>=1.30`.
- `hatch-vcs>=0.4` is part of `build-system.requires`.
- Dev tooling floors are `mypy>=2.1`, `pytest>=9.0`, and `ruff>=0.15`.
- Docs tooling floors are `mkdocs>=1.6.1`, `mkdocs-material>=9.7`, `mkdocstrings[python]>=1.0`, and `ruff>=0.15`.
- Package version is dynamic, with `[tool.hatch.version]` using `source = "vcs"`.
- The git tag `vX.Y.Z` is the single source of truth for package version.
- The PyPI JSON endpoint for `fortune-telling-core` returned 404 during the availability check.
- The built wheel contains only the importable package, dist metadata, entry point metadata, and the MIT license.
- `.agents/` and `.claude/` are excluded from Hatch build targets because they are local agent/tooling scaffolding, not package contents.
- The release extra includes `build` and `twine`; `twine check dist/*` is part of local and GitHub Actions release validation.

## Details

The dependency-floor refresh updated stale optional tooling requirements while keeping the package dependency posture minimal. The library still has no required runtime dependencies. This matches the project's zero-copyleft and deterministic-core goals.

Release versioning uses hatch-vcs rather than a static `version = "0.1.0"` string. On a clean checkout of an exact tag, hatch-vcs yields the bare version, for example `v0.1.0 -> 0.1.0`. On a dirty or untagged tree it yields a PEP 440 development version such as `0.1.dev1+g<sha>.d<date>`, which is expected and harmless for CI editable installs. The GitHub Actions CD build checkout uses `fetch-depth: 0` so hatch-vcs can see tags and full history.

`python -m build` produced both source distribution and pure-Python wheel artifacts named from the derived version. Installing the built wheel into a scratch virtual environment succeeded without runtime dependencies, and `fortune-telling-demo tarot --seed 7` executed successfully from the installed artifact. Release validation now runs `python -m twine check dist/*` before publishing so package metadata and README rendering are checked against the built artifacts.

Public artifacts intentionally exclude local agent support directories. `/.agents` contains project memory and skill files, and `/.claude` is tool compatibility scaffolding; neither is importable package code, runtime data, public documentation, or release metadata. Hatch build file selection excludes both directories for sdist and wheel construction, while the wheel also remains package-scoped through `packages = ["src/fortune_telling_core"]`.

## Files

- `pyproject.toml`: Build backend, dynamic version configuration, optional dependency floors, metadata, classifiers, build exclusions, and entry points.
- `.github/workflows/cd.yml`: Release build checkout must use full history for hatch-vcs tag discovery and runs `twine check dist/*` before artifact upload and publishing.
- `LICENSE`: MIT license included in built artifacts.
- `README.md`: Package usage and development instructions.
- `dist/`: Local build artifacts when generated.

## Test Coverage

Release-readiness validation has included:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy src tests
python -m pytest
hatch run test:check
python -m build
hatch build
python -m twine check dist/*
```

Wheel install smoke testing in a scratch virtual environment succeeded and the installed `fortune-telling-demo tarot --seed 7` command ran successfully.

## Pitfalls

- Keep `.agents/` and `.claude/` out of public artifacts unless there is an explicit packaging-policy change.
- Keep optional dependency floors current without turning package extras into a lock-file substitute.
- Do not reintroduce static package versions unless release-tag synchronization is handled another way.
