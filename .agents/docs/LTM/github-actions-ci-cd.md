# GitHub Actions CI/CD

## Summary

The repository has GitHub Actions workflows for continuous integration, PyPI delivery, and MkDocs publishing to GitHub Pages. Workflows are SHA-pinned, release builds validate package metadata with `twine check`, and the required PyPI Trusted Publisher and Pages settings have been completed by the repository owner.

## Key Facts

- Workflows live under `.github/workflows/`.
- `ci.yml` runs on push and pull request to `main` across Python 3.12, 3.13, and 3.14.
- CI mirrors the local lint gate: `ruff format --check`, `ruff check`, `mypy src tests`, then `pytest`.
- `cd.yml` publishes on a published GitHub Release and manual dispatch.
- PyPI publishing uses Trusted Publishing over OIDC with `id-token: write`, environment `pypi`, and `pypa/gh-action-pypi-publish`.
- The PyPI Trusted Publisher is registered for owner `moriyoshi`, repository `fortune-telling-core`, workflow `cd.yml`, and environment `pypi`.
- GitHub Pages source is set to GitHub Actions.
- `cd.yml` checkout uses `fetch-depth: 0` so hatch-vcs can compute the tag-derived version.
- `cd.yml` installs the release extra, builds sdist and wheel, and runs `python -m twine check dist/*` before artifact upload and publish.
- `docs.yml` builds `mkdocs build --strict` and deploys through the GitHub Pages OIDC flow.
- Every third-party action is pinned to a full 40-character commit SHA with a trailing version comment.
- Workflows were written but not committed under the no-discretionary-commit rule.

## Details

CI uses a plain `actions/setup-python` matrix rather than the Hatch matrix, because GitHub Actions already fans out the interpreter dimension. This keeps hosted CI aligned with the AGENTS.md local gate while avoiding a redundant Hatch-level Python matrix inside each job.

The CD workflow separates build and publish. The build job installs `.[release]`, runs `python -m build`, validates the generated sdist and wheel with `python -m twine check dist/*`, uploads the checked distributions as an artifact, and the publish job sends that artifact to PyPI through Trusted Publishing. The repository should not store a long-lived PyPI API token for this flow.

Docs publishing uses `configure-pages`, `upload-pages-artifact`, and `deploy-pages` rather than pushing a `gh-pages` branch. It triggers on changes to `docs/`, `src/`, `mkdocs.yml`, and `pyproject.toml`, with a `concurrency: pages` group that does not cancel an in-progress deployment.

Pinned action versions at the time of workflow creation:

| Action | Version |
|--------|---------|
| `actions/checkout` | v6.0.3 |
| `actions/setup-python` | v6.2.0 |
| `actions/upload-artifact` | v7.0.1 |
| `actions/download-artifact` | v8.0.1 |
| `pypa/gh-action-pypi-publish` | v1.14.0 |
| `actions/configure-pages` | v6.0.0 |
| `actions/upload-pages-artifact` | v5.0.0 |
| `actions/deploy-pages` | v5.0.0 |

SHAs were resolved from the GitHub API, dereferencing annotated tags to their commits. An initial pass used stale guessed tags; re-resolving against each repository's latest release corrected the pins.

## Files

- `.github/workflows/ci.yml`: Python matrix CI.
- `.github/workflows/cd.yml`: Build and PyPI publish workflow.
- `.github/workflows/docs.yml`: MkDocs build and GitHub Pages deployment.
- `AGENTS.md`: Local gate mirrored by CI.
- `pyproject.toml`: Dev, docs, and build tooling used by workflows.
- `pyproject.toml`: `release` extra includes build and twine tooling used by CD.
- `mkdocs.yml`: Documentation build configuration.

## Test Coverage

Workflow validation has included:

```text
yaml.safe_load
python -m twine check dist/*
```

A grep check also confirmed every `uses:` line carries a 40-character SHA pin with a version comment, with no floating tags or branch refs remaining.

## Pitfalls

- If the repository owner, repository name, release workflow filename, or PyPI environment changes, update the PyPI Trusted Publisher registration.
- If Pages deployment is moved or disabled, recheck repository Settings -> Pages -> Source.
- Keep `cd.yml` checkout at `fetch-depth: 0` while hatch-vcs derives versions from tags.
- Refresh action pins intentionally when upgrading actions; do not replace pinned SHAs with floating tags.
