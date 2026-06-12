# Documents for both humans and coding agents

* [README.md](./README.md)

# Documents for coding agents

* [./.agents/docs/OVERVIEW.md](./.agents/docs/OVERVIEW.md) ... project overview.
* [./.agents/docs/ARCHITECTURE.md](./.agents/docs/ARCHITECTURE.md) ... library structure and design notes.
* [./.agents/docs/JOURNAL.md](./.agents/docs/JOURNAL.md) ... chronological findings, decisions, and work history.
* [./.agents/docs/LTM/INDEX.md](./.agents/docs/LTM/INDEX.md) ... long-term memory index for durable project knowledge under `./.agents/docs/LTM/`.
* [./.agents/docs/TODO.md](./.agents/docs/TODO.md) ... open to-do items, including the current implementation handoff: extract shared solar-term/time-model code into `astronomy`, then build the Nine Star Ki backend per the `JOURNAL.md` 2026-06-12 Nine Star Ki design entry.
* [./.agents/skills/](./.agents/skills/) ... local memory-maintenance skills for consolidating `JOURNAL.md`, LTM documents, and canonical project docs.

# Rules and protocols

## General

* This repository is the home for `fortune-telling-core`, a Python library for composable fortune-telling systems.
* Keep project knowledge in the agent docs as the implementation evolves.
* Prefer existing project patterns over introducing new frameworks or conventions.
* Keep the core library deterministic, typed, and testable. Randomness should be injectable so readings can be reproduced.
* Do not bake spiritual, cultural, or localisation assumptions into shared primitives. Model traditions and interpretation systems as explicit modules.
* When a design decision is genuinely ambiguous because established schools or conventions diverge (for example the Nine Star Ki day-star escapement, a house system, or a zodiac/ayanamsa choice), expose it as a configurable option (a config enum, engine argument, or request option) with a sensible documented default, rather than hardcoding one choice. Record the selected value in `Provenance.notes` so a reading stays reproducible and auditable. Use judgement: reserve options for genuine divergence, not every default, to avoid option sprawl.
* When a durable decision, pitfall, or investigation result matters to future work, append it to `.agents/docs/JOURNAL.md`.

## File Management

* Work summaries belong under `./.agents/docs`, not under `/tmp`.
* Temporary files belong under `./.agents-workspace/tmp`, not under `/tmp`.
* Never delete user files without permission. Only safe to delete: files you created in the current session under `./.agents-workspace/tmp/`.
* Keep generated scratch artefacts out of source directories unless they are part of the requested deliverable.

## Building and Testing

* The project stack is Python 3.12+ with a `src/` package layout.
* When fixing a bug, add a focused regression test whenever the codebase has a practical test harness.
* Do not report a change as complete until the relevant checks have been run, or until you explicitly state why they could not be run.

## Local Lint Gate

Before reporting a code change as done, run the project's canonical formatter, linter, type-checker, and tests once those commands exist. Record the current commands in this section when the stack is expanded.

Current stack: Python package with `pyproject.toml`, `src/fortune_telling_core`, and `tests`.

Always use the project virtualenv at `./.venv` for Python tooling. The bare `python`/`pip` on `PATH` resolves to the pyenv-global interpreter, **not** the venv, so activate the venv (`source .venv/bin/activate`) or call the venv binaries explicitly (`./.venv/bin/python`, `./.venv/bin/pip`). Never `pip install` into the global/pyenv interpreter — this includes `build`, `twine`, `mkdocs`, and the `.[dev]`/`.[docs]`/`.[release]` extras.

Canonical commands (run after `source .venv/bin/activate`, or prefix each with `./.venv/bin/`):

* Create the virtual environment: `python3 -m venv .venv`
* Activate it: `source .venv/bin/activate`
* Install for development: `python -m pip install -e ".[dev]"`
* Format: `python -m ruff format .`
* Lint: `python -m ruff check .`
* Type-check: `python -m mypy src tests`
* Test: `python -m pytest`

The library supports Python 3.12, 3.13, and 3.14. A Hatch matrix runs the suite (and full gate) against each:

* All versions, tests only: `hatch run test:run`
* All versions, full gate (ruff + mypy + pytest): `hatch run test:check`
* A single version: `hatch run +py=3.14 test:run`

Before reporting a change that could affect cross-version behaviour as done, run `hatch run test:check` so all three interpreters are exercised.

## Shell Pitfalls (prezto defaults)

The user's shell uses prezto, which sets aliases and options that can break non-interactive scripts:

* `cp src dst` may prompt interactively when `dst` exists. Prefer explicit overwrite-safe commands.
* `cat > file <<'EOF'` and `echo > file` can fail with `file exists` when the target exists. Use the repository editing tools rather than shell redirection for tracked files.
* `rm file` may prompt for confirmation. Never delete user files unless the task explicitly requires it.

## Git Workflow

* Never make discretionary commits. Commit only when the user asks.
* If commits are requested, sign them with `-S` unless the user gives different instructions.
* Preserve unrelated work in the tree. Do not revert changes you did not make.

## Documentation

* Append new findings to `JOURNAL.md`; do not edit existing entries in place except through established memory-consolidation workflows.
* In repo-authored documentation (`AGENTS.md`, `README.md`, `.agents/docs/**`), never use full-width parentheses. Use half-width parentheses.
* Same for full-width colons. Use a half-width colon followed by a space.
