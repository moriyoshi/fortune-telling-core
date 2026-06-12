# Project Scaffold and Agent Operations

## Summary

The repository is structured as a coding-agent-ready Python package for `fortune-telling-core`. Durable project knowledge lives under `.agents/docs/`, scratch work belongs under `.agents-workspace/`, and local memory-maintenance skills live under `.agents/skills/`.

## Key Facts

- The project is a Python 3.12+ package with a `src/` layout, `pyproject.toml`, `src/fortune_telling_core`, and `tests`.
- Agent-facing docs are `AGENTS.md`, `.agents/docs/OVERVIEW.md`, `.agents/docs/ARCHITECTURE.md`, `.agents/docs/JOURNAL.md`, `.agents/docs/TODO.md`, and `.agents/docs/LTM/INDEX.md`.
- The repo now uses git on `main` with SSH-signed commits available; do not commit unless asked.
- Work summaries belong under `.agents/docs`, not under `/tmp`.
- Temporary scratch artifacts belong under `.agents-workspace/tmp`.
- LTM maintenance skills are local under `.agents/skills/`: `good-sleep`, `deep-sleep`, `distill-memories`, and `reconcile-journal-ltm`.
- Always use this repository's `./.venv` for Python tooling; bare `python` and `pip` resolve to the pyenv-global interpreter.
- Gate each repository from its own working directory with its own virtualenv.

## Details

The initial scaffold established a root `AGENTS.md`, an `.agents/docs/` documentation set, ignore rules for `.agents-workspace/`, local Claude compatibility ignore rules, and the Python package skeleton. The package grew from that scaffold into a deterministic, typed library with four traditions, shared astronomy, API docs, and a Hatch matrix.

The maintenance skills were ported from another project and adapted to this repository. They replace source-project references with `AGENTS.md`, use `fortune-telling-core` examples, and preserve the repository documentation style rules: half-width parentheses, half-width colons followed by a space, and no full-width punctuation.

The repo was not under version control for much of the initial build, so earlier coordination used single-writer discipline. Git and worktrees are now available for future parallel work.

Python tooling must run through the project virtualenv. Use `source .venv/bin/activate` or call `./.venv/bin/python` and `./.venv/bin/pip` explicitly. Do not install build, docs, release, or dev tooling into the global pyenv interpreter.

## Files

- `AGENTS.md`: Root operating guide for agents and humans.
- `.agents/docs/OVERVIEW.md`: Project overview.
- `.agents/docs/ARCHITECTURE.md`: Library structure and design notes.
- `.agents/docs/JOURNAL.md`: Append-only chronological findings and decisions.
- `.agents/docs/TODO.md`: Open project work and extracted follow-ups.
- `.agents/docs/LTM/`: Topic-oriented durable memory.
- `.agents/skills/`: Local memory-maintenance skill definitions.
- `.agents-workspace/`: Scratch workspace for temporary artifacts.

## Test Coverage

This topic is mostly operational documentation. When editing docs that affect the public site, run `.venv/bin/python -m mkdocs build --strict` if MkDocs is installed. For code-affecting changes, use the canonical local gate documented in `AGENTS.md`.

## Pitfalls

- `JOURNAL.md` is append-only outside established memory-consolidation workflows.
- Do not delete source LTM documents during `deep-sleep`; synthesis docs keep source docs for traceability.
- Do not place work summaries or durable notes under `/tmp`.
- Preserve unrelated dirty work in the tree.
- Do not run one repository's virtualenv against another repository's working directory.
- Renaming a package directory can break its virtualenv because console-script shebangs and editable-install path records contain absolute paths; recreate the venv after such a rename.
