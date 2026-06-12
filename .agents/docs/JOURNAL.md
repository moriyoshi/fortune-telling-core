# Journal

Chronological findings, review notes, and decisions. Append at the bottom; do not edit existing entries in place except through established consolidation workflows.

## LTM Consolidation Record

The journal has been audited against `.agents/docs/LTM/` and `.agents/docs/TODO.md`. Durable knowledge from the substantive journal entries listed below is represented in long-term memory or TODO, so the consolidated entries and older consolidation-record sections have been removed from this file.

| Journal Section | LTM / TODO Coverage |
|-----------------|---------------------|
| 2026-06-12 - AGPL adapter removed and MIT licence added | licensing-and-dependency-policy.md |
| 2026-06-12 - Agent framework and Python package scaffold bootstrapped | project-scaffold-and-agent-ops.md |
| 2026-06-12 - Agent scaffolding excluded from release artifacts | packaging-and-release-readiness.md, operations-quality-compliance-synthesis.md |
| 2026-06-12 - Astrology backend implemented | astrology-backend.md, computed-tradition-pattern.md |
| 2026-06-12 - BuiltinEphemeris series generation made reproducible | shared-astronomy-and-ephemeris.md, computed-traditions-astronomy-synthesis.md |
| 2026-06-12 - Core API and tarot reference implemented | core-reading-model-and-replay.md, tarot-reference.md |
| 2026-06-12 - Demo CLI added | demo-cli.md, operations-quality-compliance-synthesis.md |
| 2026-06-12 - Demo CLI locale option | demo-cli.md, core-reading-model-and-replay.md, interpreter-package-boundary.md |
| 2026-06-12 - Demo CLI naive birth datetimes use terminal timezone | demo-cli.md |
| 2026-06-12 - Design for a Four Pillars (BaZi) backend and shared astronomy extraction | four-pillars-backend.md, computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md |
| 2026-06-12 - Design for a Nine Star Ki backend and shared solar-term/time-model extraction | nine-star-ki-backend.md, computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md, TODO.md |
| 2026-06-12 - Design for a Tier-1 accurate built-in ephemeris | shared-astronomy-and-ephemeris.md, licensing-and-dependency-policy.md |
| 2026-06-12 - Design for an astrology backend | astrology-backend.md, computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md |
| 2026-06-12 - Documentation pass follow-up summary and findings | api-docs-and-quality-gate.md |
| 2026-06-12 - GitHub Actions CI/CD and docs publishing workflows added | github-actions-ci-cd.md, operations-quality-compliance-synthesis.md, TODO.md |
| 2026-06-12 - Initial design for the core API and a tarot reference | core-reading-model-and-replay.md, tarot-reference.md |
| 2026-06-12 - Integer deck weights and RWS interpretation data | tarot-reference.md, core-reading-model-and-replay.md |
| 2026-06-12 - Interpretation and locale surface removed | core-reading-model-and-replay.md, interpreter-package-boundary.md, core-engine-replay-synthesis.md |
| 2026-06-12 - Interpreter package split verified | interpreter-package-boundary.md, core-engine-replay-synthesis.md |
| 2026-06-12 - LTM maintenance skills ported | project-scaffold-and-agent-ops.md |
| 2026-06-12 - Licensing decision: no copyleft, remove the pyswisseph (AGPL) extra | licensing-and-dependency-policy.md |
| 2026-06-12 - Locale expansion plan | core-reading-model-and-replay.md, interpreter-package-boundary.md, TODO.md |
| 2026-06-12 - Locale resolver and interpretation registry started | core-reading-model-and-replay.md, interpreter-package-boundary.md |
| 2026-06-12 - MkDocs API reference docstrings populated | api-docs-and-quality-gate.md |
| 2026-06-12 - Moon latitude exposed on EclipticPosition | shared-astronomy-and-ephemeris.md, computed-traditions-astronomy-synthesis.md, TODO.md |
| 2026-06-12 - Nine Star Ki backend implemented with shared solar-term extraction | nine-star-ki-backend.md, computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md |
| 2026-06-12 - Nine Star Ki day-star escapement made configurable | nine-star-ki-backend.md, computed-tradition-pattern.md |
| 2026-06-12 - Package version switched to tag-derived (hatch-vcs) | packaging-and-release-readiness.md, github-actions-ci-cd.md |
| 2026-06-12 - Placidus semi-arc iteration implemented | astrology-backend.md, computed-traditions-astronomy-synthesis.md, TODO.md |
| 2026-06-12 - Public locale policy documented | core-reading-model-and-replay.md, interpreter-package-boundary.md |
| 2026-06-12 - Publish readiness review and dependency-floor follow-up | packaging-and-release-readiness.md, operations-quality-compliance-synthesis.md, TODO.md |
| 2026-06-12 - Python 3.12/3.13/3.14 matrix via Hatch | api-docs-and-quality-gate.md, project-scaffold-and-agent-ops.md |
| 2026-06-12 - Reading request question removed | core-reading-model-and-replay.md, core-engine-replay-synthesis.md |
| 2026-06-12 - Reading summary American-English contract | core-reading-model-and-replay.md, core-engine-replay-synthesis.md |
| 2026-06-12 - Session handoff: release validation and Moon latitude | packaging-and-release-readiness.md, shared-astronomy-and-ephemeris.md, TODO.md |
| 2026-06-12 - Session summary: TODO sweep, interpretation extraction, rename | packaging-and-release-readiness.md, core-reading-model-and-replay.md, interpreter-package-boundary.md, project-scaffold-and-agent-ops.md, operations-quality-compliance-synthesis.md |
| 2026-06-12 - Shared astronomy extraction and Four Pillars backend implemented | four-pillars-backend.md, computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md |
| 2026-06-12 - Tier-1 BuiltinEphemeris implemented | shared-astronomy-and-ephemeris.md, licensing-and-dependency-policy.md |
| 2026-06-12 - Tooling dependency floors refreshed | packaging-and-release-readiness.md, operations-quality-compliance-synthesis.md |
| 2026-06-12 - Twine check added to release validation | packaging-and-release-readiness.md, github-actions-ci-cd.md, operations-quality-compliance-synthesis.md |
| 2026-06-12 - VSOP87D sources moved to a local download cache | shared-astronomy-and-ephemeris.md, computed-traditions-astronomy-synthesis.md |
| 2026-06-12 - Work summary and cross-cutting findings | project-scaffold-and-agent-ops.md, core-reading-model-and-replay.md, computed-tradition-pattern.md, licensing-and-dependency-policy.md, TODO.md |

Open follow-up work extracted from historical journal entries is tracked in `.agents/docs/TODO.md`.

Synthesis documents:

| Synthesis Document | Source Documents |
|--------------------|------------------|
| computed-traditions-astronomy-synthesis.md | computed-tradition-pattern.md, shared-astronomy-and-ephemeris.md, astrology-backend.md, four-pillars-backend.md, nine-star-ki-backend.md |
| core-engine-replay-synthesis.md | core-reading-model-and-replay.md, computed-tradition-pattern.md, tarot-reference.md, interpreter-package-boundary.md |
| operations-quality-compliance-synthesis.md | project-scaffold-and-agent-ops.md, api-docs-and-quality-gate.md, licensing-and-dependency-policy.md, demo-cli.md, packaging-and-release-readiness.md, github-actions-ci-cd.md |

Standalone drill-down LTM documents:

| Document | Reason |
|----------|--------|
| api-docs-and-quality-gate.md | Command and documentation reference should remain directly discoverable. |
| astrology-backend.md | Backend-specific formulas, files, and tests remain useful independently. |
| computed-tradition-pattern.md | Shared computed-engine idioms remain useful as a direct implementation reference. |
| core-reading-model-and-replay.md | Core schema, replay, and serialization rules remain useful as a direct implementation reference. |
| demo-cli.md | CLI behavior and smoke-test examples are cohesive and directly discoverable. |
| four-pillars-backend.md | BaZi-specific rules and anchors are dense enough to keep separate. |
| github-actions-ci-cd.md | Workflow, pinning, and external setup details should remain directly discoverable. |
| interpreter-package-boundary.md | Namespace and package-boundary details should remain directly discoverable. |
| licensing-and-dependency-policy.md | Compliance policy should remain independently discoverable. |
| nine-star-ki-backend.md | Lo Shu and day-star escapement details should remain easy to inspect directly. |
| packaging-and-release-readiness.md | Release artifact policy and versioning details should remain directly discoverable. |
| project-scaffold-and-agent-ops.md | Agent workflow and file-management rules should remain direct. |
| shared-astronomy-and-ephemeris.md | Astronomy implementation notes, generator provenance, and accuracy pitfalls are a separate reference. |
| tarot-reference.md | Tarot is cohesive and smaller than the computed-tradition cluster. |

Relocated documents:

| Topic | Location |
|-------|----------|
| Locale and interpretation LTM | Relocated to `../fortune-telling-core-interpreter/.agents/docs/LTM/` as active documentation for the interpreter package. |

See `.agents/docs/LTM/INDEX.md` for the full LTM index.
