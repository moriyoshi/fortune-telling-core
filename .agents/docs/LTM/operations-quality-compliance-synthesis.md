# Operations Quality Compliance Synthesis

## Summary

The repository is set up for coding-agent work, strict local quality gates, generated API documentation, demo CLI smoke testing, GitHub Actions automation, and a zero-copyleft dependency posture. Operational memory is split between root instructions, canonical docs, LTM topic notes, and local memory-maintenance skills, while release readiness is governed by tag-derived versions, artifact validation, and completed external PyPI/Pages setup.

## Included Documents

| Document | Focus |
|----------|-------|
| [project-scaffold-and-agent-ops.md](./project-scaffold-and-agent-ops.md) | Repo scaffold, agent docs, scratch locations, git state, and memory skills. |
| [api-docs-and-quality-gate.md](./api-docs-and-quality-gate.md) | MkDocs, examples, canonical gates, and Hatch cross-version matrix. |
| [licensing-and-dependency-policy.md](./licensing-and-dependency-policy.md) | MIT license, zero-copyleft policy, removed Swiss Ephemeris surface, and dependency posture. |
| [demo-cli.md](./demo-cli.md) | `fortune-telling-demo`, deterministic sample requests, JSON output, and timezone handling. |
| [packaging-and-release-readiness.md](./packaging-and-release-readiness.md) | Dependency floors, tag-derived versions, build artifacts, and pre-alpha release caveats. |
| [github-actions-ci-cd.md](./github-actions-ci-cd.md) | GitHub Actions CI, PyPI delivery, GitHub Pages publishing, SHA-pinned actions, and completed external setup. |

## Stable Knowledge

- The project is a Python 3.12+ `src/` layout package.
- Agent-facing docs live under `.agents/docs/`; scratch work belongs under `.agents-workspace/`.
- Local memory skills live under `.agents/skills/`.
- The repo uses git on `main`; do not commit unless asked.
- Python tooling must run through this repository's `./.venv`; bare `python` and `pip` resolve to the pyenv-global interpreter.
- Gate each repository from its own working directory with its own virtualenv.
- Required runtime dependencies are empty.
- The package is MIT and must stay zero-copyleft for commercial closed-source consumption.
- MkDocs and mkdocstrings render the public API docs.
- Hatch runs the Python 3.12, 3.13, and 3.14 matrix.
- `fortune-telling-demo` is the dependency-free console smoke-test and demonstration surface.
- Build, dev, and docs tooling versions are lower-bound extras or build requirements, not application lock pins.
- Package version is derived from git tags through hatch-vcs; `vX.Y.Z` is the release version source of truth.
- Release validation includes `python -m twine check dist/*` through the `release` extra.
- `.agents/` and `.claude/` are excluded from public package artifacts.
- GitHub Actions workflows use SHA-pinned third-party actions with trailing version comments.
- PyPI release uses Trusted Publishing over OIDC; the repo should not store a long-lived PyPI API token.
- The PyPI Trusted Publisher and GitHub Pages source setup have been completed by the repository owner.

## Operational Guidance

Before changing code, read the relevant root and `.agents/docs/` context. Preserve unrelated dirty work. Put durable findings in `JOURNAL.md` or LTM through the documented workflows; do not place durable summaries under `/tmp`.

For docs affecting the public site, run the MkDocs strict build when available. For code-affecting changes, run the canonical local gate. For cross-version behavior, run the Hatch matrix.

Activate the project virtualenv or call `./.venv/bin/python` explicitly before running Python tooling. Do not install build, docs, release, or dev tooling into the global pyenv interpreter. If work crosses into the sibling interpreter repository, switch cwd and use that repository's own virtualenv and gate commands.

For dependencies or astronomy precision work, preserve the zero-copyleft posture. Use bring-your-own integrations behind protocols when consumers need licensed or higher-precision backends.

Use `fortune-telling-demo` as a quick installed-artifact smoke test, especially after packaging or entry-point changes. For computed demos, keep inputs explicit and deterministic; naive CLI birth datetimes are interpreted at the argument boundary in the terminal or system timezone.

For releases, tag from git rather than editing a static version. Keep `.github/workflows/cd.yml` checkout at `fetch-depth: 0` so hatch-vcs can see tags and full history. Keep local support material such as `.agents/` and `.claude/` out of public artifacts, and run `twine check` in an environment that has `twine`.

## Files

- `AGENTS.md`: Root operating guide and canonical commands.
- `.agents/docs/`: Overview, architecture, journal, TODO, and LTM.
- `.agents/skills/`: `good-sleep`, `deep-sleep`, `distill-memories`, and `reconcile-journal-ltm`.
- `.agents-workspace/`: Agent scratch space.
- `docs/`, `mkdocs.yml`: API documentation site.
- `pyproject.toml`: Package metadata, dynamic version configuration, console script, dev/docs extras, and Hatch matrix.
- `LICENSE`: MIT license.
- `README.md`: User-facing project overview and licensing posture.
- `src/fortune_telling_core/cli.py`: Demo CLI implementation.
- `.github/workflows/ci.yml`: Python matrix CI.
- `.github/workflows/cd.yml`: Build and PyPI publish workflow.
- `.github/workflows/docs.yml`: MkDocs build and GitHub Pages deployment.

## Tests

Canonical local gate:

```bash
python -m ruff format .
python -m ruff check .
python -m mypy src tests
python -m pytest
```

Cross-version gate:

```bash
hatch run test:check
```

Docs gate:

```bash
.venv/bin/python -m mkdocs build --strict
```

Packaging and workflow checks:

```bash
python -m build
hatch build
python -m twine check dist/*
fortune-telling-demo tarot --seed 7
```

Workflow files have been parsed with `yaml.safe_load`, and grep checks have confirmed that every `uses:` line carries a 40-character SHA pin with a version comment.

## Pitfalls

- Do not delete source LTM documents during `deep-sleep`.
- Do not edit `JOURNAL.md` entries in place outside established consolidation workflows.
- Do not run one repository's virtualenv against another repository's working directory.
- Recreate a virtualenv after renaming a package directory because editable-install records and console-script shebangs contain absolute paths.
- Do not reintroduce `pyswisseph`, Swiss Ephemeris adapters, or other copyleft surfaces without an explicit licensing decision.
- Optional dependencies can still create compliance risk.
- Material for MkDocs may print its upstream MkDocs 2.0 advisory; treat the command exit status and strict warnings as the project signal.
- Recheck PyPI Trusted Publisher registration if the owner, repository, workflow filename, or environment changes.
- Recheck repository Settings -> Pages -> Source if docs publishing stops using GitHub Actions.
- Do not replace SHA-pinned actions with floating tags when refreshing workflow dependencies.
- Do not reintroduce static package versions unless release-tag synchronization is handled another way.
