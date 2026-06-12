# Long-Term Memory Index

Durable topic documents distilled from `.agents/docs/JOURNAL.md`, plus synthesis documents that consolidate overlapping topics.

## Synthesis Documents

| Document | Summary |
|----------|---------|
| [computed-traditions-astronomy-synthesis.md](computed-traditions-astronomy-synthesis.md) | Consolidates computed-tradition replay, shared astronomy, and the astrology, Four Pillars, and Nine Star Ki backends. |
| [core-engine-replay-synthesis.md](core-engine-replay-synthesis.md) | Consolidates the core replay model, computed-tradition engine pattern, tarot as the random-draw reference, and the interpreter package boundary. |
| [operations-quality-compliance-synthesis.md](operations-quality-compliance-synthesis.md) | Consolidates agent operations, API docs and quality gates, demo CLI, packaging/release readiness, GitHub Actions, and licensing/dependency policy. |

## Source Topic Documents

| Document | Summary |
|----------|---------|
| [api-docs-and-quality-gate.md](api-docs-and-quality-gate.md) | MkDocs API docs, examples, canonical local gates, and Hatch cross-version testing. |
| [astrology-backend.md](astrology-backend.md) | Natal astrology backend design, files, replay behavior, house systems, aspects, and tests. |
| [computed-tradition-pattern.md](computed-tradition-pattern.md) | Shared `cast()`/`NullRng` idiom, ephemeris-free replay, summary-only derived data, and provenance notes. |
| [core-reading-model-and-replay.md](core-reading-model-and-replay.md) | Core primitives, engine contract, serialization, deterministic RNG, provenance, and replay guarantees. |
| [demo-cli.md](demo-cli.md) | Demo CLI commands, serialized output, and timezone handling for naive birth datetimes. |
| [four-pillars-backend.md](four-pillars-backend.md) | Four Pillars backend rules, shared solar-term use, Ten Gods, luck pillars, time models, and tests. |
| [github-actions-ci-cd.md](github-actions-ci-cd.md) | GitHub Actions CI, PyPI delivery, GitHub Pages publishing, SHA-pinned actions, and completed external setup. |
| [interpreter-package-boundary.md](interpreter-package-boundary.md) | Boundary between structural core readings and the sibling interpretation/localization package. |
| [licensing-and-dependency-policy.md](licensing-and-dependency-policy.md) | MIT and zero-copyleft policy, AGPL adapter removal, and bring-your-own ephemeris boundary. |
| [nine-star-ki-backend.md](nine-star-ki-backend.md) | Nine Star Ki stars, Lo Shu charts, solar-term boundaries, tendency logic, and day-star escapement options. |
| [packaging-and-release-readiness.md](packaging-and-release-readiness.md) | Dependency floors, tag-derived versions, build artifacts, no-runtime-dependency posture, and release caveats. |
| [project-scaffold-and-agent-ops.md](project-scaffold-and-agent-ops.md) | Repository scaffold, agent docs, memory-maintenance skills, scratch locations, and git/worktree state. |
| [shared-astronomy-and-ephemeris.md](shared-astronomy-and-ephemeris.md) | Shared astronomy package, ephemeris protocol, Tier-1 `BuiltinEphemeris`, solar helpers, and boundary pitfalls. |
| [tarot-reference.md](tarot-reference.md) | Tarot reference engine, RWS deck and spreads, reversals, and integer weights. |

## Relocated Documents

| Topic | Location |
|-------|----------|
| Locale and interpretation LTM | Relocated to `../fortune-telling-core-interpreter/.agents/docs/LTM/` as active documentation for the interpreter package. |
