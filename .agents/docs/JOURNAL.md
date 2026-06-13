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

## 2026-06-12 - Interpreter packaging prep

Split interpreter packaging prep: made core packages pkgutil namespaces and promoted coerce/serde_types helper modules for external namespace contributors.

## 2026-06-13 - Zodiac date utilities (dates.py, Sign enum)

Added zodiac date utilities (new `dates.py`): `zodiac_date_range(sign)` returns conventional Western-tropical `((month, day), (month, day))` bounds, and `sign_for_date(date)` classifies a date to a sign id. Chose `(month, day)` tuples over a "days since 1/1" offset because a fixed offset is leap-year-ambiguous (10 of 12 boundaries shift after Feb 29); `sign_for_date` compares on `(month, day)` so it is leap-correct by construction. Introduced `Sign(StrEnum)` in `zodiac.py` as the single source of truth for the 12 signs and their order, killing the slug list that was duplicated in `zodiac.py`/`houses.py`/`dates.py`; decks, `sign_id()`, and all serialized data are unchanged (verified), so the change is additive/backwards-compatible. Note: enum accessor is `.ordinal` not `.index`, since `StrEnum` subclasses `str` and `index` would violate LSP under `mypy --strict`. These utilities are deliberately NOT on the horoscope-reading critical path — the engine computes sun signs astronomically from `cast()`; the table is for offline/UI use. Committed on branch `add-zodiac-date-utilities` (8ba9006).

## 2026-06-13 - Thaksa and Can Chi traditions

Added two new dependency-free, birth-driven traditions — Thai **Thaksa** (`traditions/thaksa/`) and Vietnamese **Can Chi** (`traditions/can_chi/`) — both modeled on the weton/four_pillars deterministic shape (`cast()`/`replay()`, `NullRng` guard, structural-only summary, no interpretation). **Thaksa**: deck = 8 grahas (planets), spread = 8 houses (บริวาร…กาลกิณี); the engine seats the 8 grahas into the houses starting from the birth-day ruler, cycling in the canonical Thaksa order Sun→Moon→Mars→Mercury→Saturn→Jupiter→Rahu→Venus. Findings: verified the cycle order, the 8-house order, planetary strengths (กำลัง: Sun 6, Moon 15, Mars 8, Mercury 17, Saturn 10, Jupiter 19, Rahu 12, Venus 21), and that a Wednesday birth ≥18:00 rules under Rahu (Wednesday-night, พุธกลางคืน) — the 8th "day". The Wednesday day/night split is a planet swap only; it does NOT roll the weekday to Thursday (so I deliberately did not add a weton-style DayBoundary). Cross-checked the canonical Sunday arrangement (Boriwan=Sun … Kalakini=Venus). **Can Chi**: Vietnamese sexagenary day+hour pillars (Thiên Can ×10, Địa Chi ×12, con giáp animals incl. the distinctively Vietnamese Mèo/Cat and Trâu/Water-Buffalo). Key decision: reused Four Pillars' exact day anchor (1984-02-02 = Giáp Tý, via the shared pure `astronomy.julian.julian_day_from_date`) and the five-rat hour-stem rule, so Can Chi and Four Pillars agree on every calendar day — asserted by a cross-validation test sweeping 400 days against `four_pillars.sexagenary`. Both day & hour pillars are pure calendar arithmetic (no ephemeris), unlike four_pillars. Deliberately **omitted the year pillar (tuổi con giáp)**: the year rolls over at Tết (lunar new year), which a dependency-free engine cannot locate without a lunar table — documented in the engine docstring so the gap is explicit rather than silently approximated. Slug collision note: Tý (Rat) and Tỵ (Snake) both romanize to "ty"; the snake uses slug "ti" to keep symbol ids unique. New tests: `tests/traditions/thaksa/` + `tests/traditions/can_chi/` (26 tests). Full suite 142 passed; `mypy --strict` + `ruff` clean. Branch `add-thai-vietnamese-traditions`.

## 2026-06-13 - Weton (Primbon) tradition

Added the Javanese **weton** (Primbon) tradition under `traditions/weton/` — the Indonesian birth-sign system pairing the 7-day week (*saptawara*) with the 5-day market week (*pancawara*/pasaran) and summing their *neptu*. Modeled on `four_pillars`/`nine_star_ki` (deterministic, birth-date-driven `cast()`/`replay()`, `NullRng` guard, structural-only summary), but pure calendar arithmetic so it adds **no runtime deps** (no ephemeris). Deck = 12 symbols (7 days + 5 pasaran); spread = 2 positions (`saptawara`, `pancawara`); selections carry neptu modifiers and combined weton neptu. Key findings: (1) Pancawara has no civil anchor, so I anchored the 5-day phase to **17 Aug 1945 = Jumat Legi** (Proclamation of Independence, neptu 11) and read saptawara straight from the proleptic Gregorian weekday. Verified the phase against authoritative Indonesian sources — proclamation weton, and ki-demang almanac giving 1 Jan 2000 = Sabtu Legi (my initial memory of "Sabtu Pon" was wrong by 2 cycle-steps; the web check caught it). (2) The Javanese day begins at *sunset*, not midnight, so evening births can roll to the next weton; true sunset needs location, so I exposed this as a `DayBoundary` option (`midnight` default / `sunset` ≈ 18:00 local-clock threshold) rather than hardcoding, per the "surface ambiguity as API options" convention. Chosen rule is recorded in provenance notes alongside the anchor. Full suite 116 passed; `mypy --strict` + `ruff` clean. Branch `add-weton-tradition` (PR #3).

## 2026-06-13 - Tzolk'in tradition (/loop iteration 1)

Added the Maya **Tzolk'in** tradition (`traditions/tzolkin/`) — the 260-day sacred round (20 day signs × 13 trecena numbers). Deterministic, dependency-free, anchor-based like weton/can_chi. Deck = 20 day signs (Yucatec names + English keyword + cardinal direction East/North/West/South cycling); spread = 1 position (`day_sign`) carrying the trecena number 1-13 as a modifier; a day is named "<number> <sign>" e.g. "4 Ajaw". Finding: anchored the round to **21 Dec 2012 = 4 Ajaw** under the **GMT (Goodman-Martínez-Thompson) correlation, constant 584283** — the most widely accepted; verified that 2012-12-21 is exactly 13.0.0.0.0 (delta from anchor 1872000 = 13×144000 baktuns) and that the pairing repeats every 260 days. Number and sign advance independently (+1/day, mod 13 and mod 20). Correlation choice is recorded in provenance notes so an alternate correlation could be added later as an option. 10 new tests; `mypy --strict` + `ruff` clean. Branch `add-more-traditions`.

## 2026-06-13 - Pythagorean numerology tradition (/loop iteration 2)

Added **Pythagorean numerology** (`traditions/numerology/`) — deterministic birth-date reduction, dependency-free. Deck = 12 numbers (1-9 + master numbers 11/22/33, each with a keyword); spread = 2 positions (`life_path`, `birthday`). Life Path is reduced from the full date; Birthday from the day of month; both preserve masters via `reduce_number` (loops digit-sum until ≤9 or in {11,22,33}). Key decision (surface-ambiguity-as-options): the two common Life Path methods diverge on master numbers, so I exposed a `ReductionMethod` config — **COMPONENT** (reduce month/day/year separately, then sum; default, the method most numerologists call correct) vs **ITERATIVE** (sum all digits at once). Finding: divergence runs *both* ways — e.g. 1985-09-01 gives COMPONENT=6 but ITERATIVE=33 (the all-at-once sum lands exactly on a master that the component method dissolves), so neither method uniformly preserves more masters; verified and pinned in a test. Chosen method recorded in provenance notes. 18 new tests; `mypy --strict` + `ruff` clean; full suite 130 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Haab' tradition (/loop iteration 3)

Added the Maya **Haab'** tradition (`traditions/haab/`) — the 365-day vague year (18 winal × 20 days + the 5-day Wayeb'), the Tzolk'in's partner in the Calendar Round. Deterministic, dependency-free, same GMT-correlation anchor as iter-1's Tzolk'in. Deck = 19 months (18 winal + Wayeb', each with its length); spread = 1 position (`haab`) carrying the 0-based day position; a date reads "<day> <month>" e.g. "3 K'ank'in". Findings: anchored to **21 Dec 2012 = 3 K'ank'in** (year position 13×20+3 = 263), the Haab' partner of 13.0.0.0.0 4 Ajaw; used the **0-based epigraphic day numbering** (seating of a month = day 0, so Wayeb' runs 0–4), and verified the year boundary (4 Wayeb' → 0 Pop, the Haab' new year) and the 365-day period. The engine flags Wayeb' (the 5 unlucky days) in the summary. 12 new tests; `mypy --strict` + `ruff` clean. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Celtic tree calendar tradition (/loop iteration 4)

Added the **Celtic tree calendar** / Ogham tree zodiac (`traditions/celtic_tree/`) — a date-range birth-sign classifier (like the Western zodiac), deterministic and dependency-free. Deck = 13 signs (Ogham letter + tree + date range, e.g. Duir/Oak); spread = 1 position (`tree_sign`). Honesty note recorded in code + provenance: this is **Robert Graves' 20th-century reconstruction** (*The White Goddess*, 1948), not an attested ancient Celtic calendar — flagged so we don't overstate authenticity. Key decisions/findings: (1) Graves leaves **23 Dec as a "nameless day"** outside the 13 months; to make classification *total* I folded it into the preceding sign Ruis/Elder (range 25 Nov–23 Dec) and recorded `nameless_day=folded-into-ruis` in provenance. (2) Ranges are fixed `(month, day)` tuples compared as tuples, so leap-year correct by construction (reused the zodiac `dates.py` insight from the 2026-06-13 entry); Beth/Birch wraps the year-end (24 Dec–20 Jan). Verified all 366 leap-year days classify to exactly one of the 13 signs and ranges are contiguous. 17 new tests; `mypy --strict` + `ruff` clean; full suite 159 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Elder Futhark runes tradition (/loop iteration 5)

Added **Elder Futhark runes** (`traditions/runes/`) — first RNG-drawn addition in this loop (the prior four were deterministic birth-date systems); mirrors the tarot engine shape (`read(request, rng=...)`, `shuffle` + optional `allow_reversals`), not `cast()`. Deck = 24 runes (glyph ᚠ…ᛟ, transliteration, ætt, keyword) in the three ættir; spreads = `SINGLE_RUNE` and `NORNS` (Urðr/Verðandi/Skuld past-present-future). Rune-specific value-add: the **merkstave rule** — the 8 runes symmetrical under a 180° turn (Gebo, Hagalaz, Isa, Jera, Eihwaz, Sowilo, Ingwaz, Dagaz) have no reversed form, flagged `reversible=false` and forced upright even when reversals are on. Design note: when reversals are enabled I consume one `rng.random()` *per position regardless* of reversibility, so the RNG stream stays aligned/predictable; the reversibility flag only gates whether the consumed roll can produce a "reversed" orientation. Verified via SequenceRng that a reversible rune (Fehu) turns on roll 0.0 while a symmetrical rune (Isa) stays upright on the same roll, plus read→replay→serde determinism. 7 new tests; `mypy --strict` + `ruff` clean; full suite 166 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - I Ching tradition (/loop iteration 6)

Added the **I Ching** (`traditions/iching/`) — RNG-drawn like tarot/runes but with a genuinely new mechanic: the three-coin cast produces six lines, a **primary hexagram**, and (by transforming the changing lines) a **relating hexagram**. Deck = 64 hexagrams (King Wen number, pinyin, English, lower/upper trigram, Yijing-block glyph ䷀…䷿ at U+4DC0+n−1, 6-bit binary); spread = 2 positions (`primary`, `relating`). Casting: each line = sum of 3 coins (heads 3 / tails 2 via `rng.random()<0.5`) → 6 old-yin(changing), 7 young-yang, 8 young-yin, 9 old-yang(changing); line is yang iff odd, changing iff 6 or 9; relating bit = yang XOR changing. Data-correctness approach (the risky part): I **fetched the King Wen table from Wikipedia** (number + lower/upper trigram for all 64) rather than trusting memory, then **verified programmatically** that deriving each hexagram's 6-bit value from its trigrams yields a perfect bijection onto 0..63 (this alone proves no lower/upper swap or duplicate) plus 7 hand-checked anchors (1=all-yang, 2=all-yin, 11 Tai, 12 Pi, 29 Kan, 63 Jiji, 64 Weiji). That bijection invariant is pinned as a test. Verified all-old-yang → Qian(1) changing into Kun(2), all-old-yin → Kun→Qian, all-young → no changing lines (relating==primary), plus read→replay→serde. 16 new tests; `mypy --strict` + `ruff` clean; full suite 182 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Petit Lenormand tradition (/loop iteration 7)

Added **Petit Lenormand** (`traditions/lenormand/`) — RNG-drawn 36-card deck (Rider…Cross in canonical order), mirroring the tarot engine. Spreads: `SINGLE_CARD`, `THREE_CARD` (left/centre/right line), and `GRAND_TABLEAU` (36 positions consuming the whole deck — the distinctive Lenormand layout). No reversals (Lenormand cards aren't read inverted), so draws carry no orientation. Decisions: (1) omitted the playing-card insets — they vary by publisher, so I kept only the universal number+name to avoid baking one uncertain mapping (consistent with the surface-ambiguity convention). (2) Process note: I first attempted **Western geomancy** this iteration but **deferred it** — the mechanic (4 RNG mothers → daughters by transpose → nieces/witnesses/judge via geomantic addition = bitwise XOR) is clear, but I could not verify the 16-figure name↔bit-pattern table to my correctness bar: both Wikipedia fetches (`Geomancy`, `Geomantic_figures`) return the patterns as images the extractor couldn't read, and a bijection check alone wouldn't catch a wrong name→pattern assignment. Geomancy remains a strong future candidate once I have a verified textual figure table. 7 new tests; `mypy --strict` + `ruff` clean; full suite 189 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Pythagorean name numerology tradition (/loop iteration 8)

Added **Pythagorean name numerology** (`traditions/name_numerology/`) — deterministic, dependency-free, certain data (no external lookup needed). Computes the three core name numbers: **Expression** (all letters), **Soul Urge** (vowels), **Personality** (consonants), each reduced keeping masters 11/22/33. Reuses the birth-date `numerology` tradition's `reduce_number` and `NUMBERS` keyword data (DRY) under its own deck/symbol ids; spread = 3 positions. Letter values are alphabet-position mod 9 (A=1…I=9, J=1…R=9, S=1…Z=8). Decision (surface-ambiguity-as-options): the **Y-as-vowel** question genuinely divides numerologists, so I exposed a `YMode` config (CONSONANT default / VOWEL); verified divergence on "Amy" — consonant mode → Soul Urge 1 / Personality 11 (Y joins M into a master number), vowel mode → Soul Urge 8 / Personality 4. Input is a `name` attribute; raises ValidationError on empty/letterless names and on names with no vowels (or no consonants) under the chosen Y mode (e.g. "Lynn" in consonant mode). Process note: I again considered **geomancy** but kept it deferred — still no image-free source for the 16-figure table, and I won't ship an unverified name↔pattern mapping. 10 new tests; `mypy --strict` + `ruff` clean; full suite 199 passed. Branch `add-more-traditions` (PR #5).

## 2026-06-13 - Western geomancy tradition (/loop iteration 9)

Added **Western geomancy** (`traditions/geomancy/`) — the previously-deferred tradition, now implemented after verifying the figure data. RNG-drawn: four **Mother** figures are generated from random points (16 rows), then **Daughters** = the Mothers' transpose, **Nieces/Witnesses/Judge** follow by geomantic addition (= bitwise XOR of the 4 rows). Deck = 16 figures (Fire/Air/Water/Earth rows, ruling element, point count); spread = 15 shield positions (4 mothers, 4 daughters, 4 nieces, 2 witnesses, judge). **How I finally verified the 16-figure table** (the thing that blocked iters 7-8): a WebSearch surfaced the four top-row elemental groups (fixing Fire+Air rows for all 16) plus two explicit anchors ("Via is Fire-on-Fire", "Albus is Earth-on-Water"); combining that with the five classical inversion pairs (Puer/Puella, Caput/Cauda, Albus/Rubeus, Laetitia/Tristitia, Amissio/Acquisitio) uniquely determines every figure. I then cross-checked four independent invariants, ALL consistent: (1) bijection onto 0..15, (2) five anchors, (3) five inversion pairs reverse-row, (4) top-element groups match the published grouping. Crucially I also brute-forced the classical theorem that **the Judge always has an even number of points** across ALL 65 536 mother-sets — this validates the entire shield computation (transpose + XOR chain), not just the table. Both the bijection and the judge-even theorem (200 seeds) are pinned as tests. 20 new tests; `mypy --strict` + `ruff` clean; full suite 219 passed. Branch `add-more-traditions` (PR #5). Lesson: when a primary source only has image data, a convergent set of structural invariants (bijection + inversions + a parity theorem) can establish correctness more rigorously than transcription would.

## 2026-06-13 - Domino divination tradition (/loop iteration 10)

Added **domino divination** (`traditions/dominoes/`) — RNG-drawn, mirroring the tarot engine, chosen for fully certain data (no anchor/correlation/table to verify) while staying structurally distinct from the card and rune decks. Deck = the 28 tiles of a double-six set, generated by pure combinatorics (all unordered pip pairs 0-6, high≥low); each tile carries high/low pips, total pip count, and a `double` flag. Spreads: `SINGLE_TILE` and `THREE_TILES` (past/present/future). No orientation. Verified the set is exactly 28 tiles with 7 doubles and unique ids, plus read→replay→serde determinism. 7 new tests; `mypy --strict` + `ruff` clean; full suite 226 passed. Branch `add-more-traditions` (PR #5). Loop status: 10 traditions landed across deterministic birth-date/name systems, a date-range classifier, and RNG-drawn casting; high-confidence candidate pool is now nearly exhausted (remaining ideas — Mayan Lords of the Night, Aztec Tōnalpōhualli, feng-shui Kua, Chinese/Tibetan year animals — each carry an anchor/correlation or lunar-boundary uncertainty I won't ship unverified), so future iterations should either invest in verifying one of those or wind down rather than pad with low-confidence data.

## 2026-06-13 - Chaldean numerology tradition (/loop iteration 11)

Added **Chaldean numerology** (`traditions/chaldean_numerology/`) — deterministic, dependency-free, certain data; a genuinely distinct sibling to the Pythagorean name numerology of iter-8. Two differences encode the system's identity: (1) the **Chaldean letter values are 1-8 only** — nine was held sacred and never assigned to a letter (verified the 8 groups cover all 26 letters exactly once and the value set is {1..8}); (2) the single-digit **root carries a planetary ruler** (Cheiro's system: 1 Sun, 2 Moon, 3 Jupiter, 4 Uranus, 5 Mercury, 6 Venus, 7 Neptune, 8 Saturn, 9 Mars). Reduces the full name's letter sum to a root 1-9 (no master numbers, unlike Pythagorean). Deck = 9 planetary numbers; spread = 1 position (`name_number`); modifiers carry the root, planet, and pre-reduction total. Nice cross-system contrast verified in tests: "John" = Chaldean root 9/Mars (total 18) vs Pythagorean Expression 2. 14 new tests; `mypy --strict` + `ruff` clean; full suite 240 passed. Branch `add-more-traditions` (PR #5). Reliable candidate pool after this: a Personal Year number (deterministic) and 52-card cartomancy remain; the culturally-iconic remainders (Chinese/Vietnamese/Tibetan year animals, Aztec/Mayan-Lords correlations) still need a lunar boundary or an anchor I won't ship unverified.

## 2026-06-13 - User-facing docs synced to full tradition set

Synced user-facing docs to the full tradition set. The README "Included Systems", `docs/index.md` Layout section, and the mkdocs nav had all drifted — they still listed only the original four (`tarot`, `astrology`, `four_pillars`, `nine_star_ki`) while the package had grown to 18 traditions. Reframed all three to group by mechanic: **Drawn** (caller-provided RNG via `read`: tarot, lenormand, dominoes, runes, geomancy, iching) vs **Computed** (birth/identity data via `cast`: astrology, four_pillars, nine_star_ki, numerology, name_numerology, chaldean_numerology, can_chi, thaksa, weton, celtic_tree, haab, tzolkin) — the same split the engines actually expose. Added the 14 missing `docs/api/traditions/*.md` pages (each = title + one-line description + a runnable example sourced from the module docstring + a `::: module` mkdocstrings directive) and split the nav Traditions section into Drawn/Computed subgroups. Example snippets were lifted from each tradition's `__init__` docstring, so the deck/spread constant names and attribute keys match the real API. `mkdocs build --strict` passes (resolves all 18 `:::` references with no broken links).

## 2026-06-13 - Non-ASCII name numerology design drafted

Drafted `.agents/docs/design/non-ascii-name-numerology.md` after reviewing the current Latin-only
`name_numerology` and `chaldean_numerology` scope. The proposal keeps existing Latin A-Z engines
explicit, avoids generic Unicode transliteration, and recommends separate script-native modules for
Hebrew gematria, Arabic Abjad, Greek isopsephy, and CJK stroke onomancy. Key decisions: engines
should reject unsupported meaningful characters rather than silently dropping them, stamp normalized
input plus per-character value traces into `Selection.modifiers`, and record script, normalization,
variant table, and disputed options in `Provenance.notes`. Follow-up refinement: separate reusable
letter, character, and stroke value systems from public fortune-telling tradition engines, so
tables such as Latin Pythagorean, Hebrew gematria, Arabic Abjad, Greek isopsephy, and CJK stroke
providers can be reused without conflating them with `Engine` implementations. CJK stroke onomancy
should start with request-supplied stroke counts or an injectable provider rather than bundling a
large stroke table.

## 2026-06-13 - Name value systems and non-ASCII numerology engines

Shipped the name-value-systems implementation on branch `name-value-systems` around the two-layer split from the proposal: reusable private value systems live under `traditions/_name_values` with shared text normalization utilities in `traditions/_name_text.py`, while public modules remain tradition engines with finite decks, spreads, provenance, and replayable `Selection.modifiers`. A separate agent landed the first slice before this work began, extracting Latin Pythagorean name values and adding the Hebrew gematria raw-total system, and that slice was already green before I started. This pass then added Greek isopsephy, Arabic Abjad, Old Cyrillic / Church Slavonic numerals, modern Cyrillic Pythagorean numerology, CJK request-supplied stroke five-grid onomancy, the Latin `accent_fold` normalization option, and the Chaldean letter-table extraction into `_name_values.latin_chaldean` with public behavior preserved. Raw-total systems use the settled structural-deck strategy: one generic result symbol in a small finite deck, with the actual unbounded total stamped in `Selection.modifiers` rather than enumerating totals as deck symbols. New systems follow the No-Silent-Loss rule, rejecting unsupported meaningful letters unless an explicit, recorded option handles them, while existing Latin default ignore behavior remains compatibility-preserved unless opted into stricter normalization. The Greek and Arabic letter-value tables were verified against source references via Wikipedia for Greek alphabetic numerals and Abjad numerals respectively, and no value-table uncertainty or deferred implementation decision remained. Verification status was clean: `mypy`, `ruff check`, and `ruff format` all passed, `pytest` reported 390 passing tests, and `hatch run test:check` was green across Python 3.12, 3.13, and 3.14.


## 2026-06-13 - Excluded the Arabic Abjad engine on cultural-sensitivity grounds

Removed the Arabic Abjad numerology engine that had just been implemented on branch `name-value-systems`. Abjad numerology is an Arabic/Islamic-associated divination system, and fortune-telling carries a strongly condemning religious context for Muslim audiences, so shipping it is inappropriate — the same rationale that dropped the `ur-IN` locale in the interpreter package. Deleted the engine package `traditions/arabic_abjad/` (deck/spreads/engine/__init__), the value system `traditions/_name_values/arabic_abjad.py`, and `tests/traditions/arabic_abjad/`. The engine was self-contained (no central registry, no docs/README/mkdocs references yet), so no other code changed; the design note's Arabic Abjad section was annotated as Excluded — do not implement so the proposal does not invite re-adding it. The other new engines (Hebrew gematria, Greek isopsephy, both Cyrillic systems, CJK request-stroke) were left in place — this exclusion is specific to the Arabic/Islamic divination context, not a blanket script policy. Gate green after removal: mypy + ruff clean, 372 tests passing (down from 390 with the 18 Abjad tests gone).

---

---

## 2026-06-13 - Embedded design note: Non-ASCII Name Numerology Proposal

Full text of `.agents/docs/design/non-ascii-name-numerology.md`, embedded here for the record.

# Non-ASCII Name Numerology Proposal

Status: Proposal only

## Problem

The current name-based numerology modules are intentionally Latin A-Z systems:

- `name_numerology` implements Pythagorean letter values.
- `chaldean_numerology` implements Chaldean letter groups.

Both modules currently fold case and ignore any character outside ASCII A-Z. That is acceptable for a narrow Latin-script contract, but it is not a correct extension point for names written with accents, Hebrew, Arabic, Greek, CJK characters, Indic scripts, or Korean Hanja. Treating every script as transliterated Latin would erase tradition-specific rules and make readings hard to audit.

Name-based numerology for non-ASCII names should therefore be modeled as explicit tradition engines built on reusable letter, character, or stroke value systems. The value systems should expose deterministic numeric traces; the tradition engines should decide which positions, reductions, grids, summaries, and provenance notes make a reading.

## Goals

- Preserve the existing Latin Pythagorean and Chaldean behavior unless a caller opts into a new mode or a new engine.
- Separate reusable letter, character, and stroke value systems from fortune-telling tradition engines.
- Support script-native name and word-number systems without forcing them into one generic numerology model.
- Keep calculations deterministic, typed, dependency-light, and replayable through stamped selection modifiers.
- Record script, normalization, variant tables, and disputed options in `Provenance.notes`.
- Avoid silently dropping meaningful letters or characters in new value systems; preserve current Latin engine behavior until a major release or explicit opt-in changes it.
- Keep interpretation text outside core; expose structural numbers and summary only.

## Non-Goals

- Do not create a universal Unicode numerology engine or universal Unicode value table.
- Do not infer cultural identity or script rules from a name automatically.
- Do not transliterate names by default.
- Do not bundle large, uncertain, or licensed stroke-count databases without a separate review.
- Do not make the top-level package re-export tradition modules.

## Design Principles

### Two-Layer Model

The implementation should distinguish two responsibilities:

- Value systems: deterministic calculators that normalize input and assign numeric values to letters, characters, or strokes.
- Tradition engines: `Engine` implementations that use one or more value systems to build a `Draw`, `Reading.summary`, and `Provenance`.

Avoid calling the lower layer an engine in code, because `Engine` already has a specific core meaning. Use names such as `NameValueSystem`, `LetterValueTable`, `CharacterValueProvider`, or `StrokeCountProvider`.

Example lower-layer protocol:

```python
class NameValueSystem(Protocol):
    id: str
    version: str

    def normalize(self, text: str, options: Mapping[str, str]) -> NormalizedName: ...
    def values(self, name: NormalizedName) -> tuple[NameValueUnit, ...]: ...
```

Example layering:

- `latin_pythagorean` value system -> `name_numerology` tradition engine.
- `latin_chaldean` value system -> `chaldean_numerology` tradition engine.
- `hebrew_standard_gematria` value system -> a future Hebrew gematria reading engine.
- `arabic_abjad` value system -> a future Abjad reading engine.
- `greek_isopsephy` value system -> a future isopsephy reading engine.
- CJK stroke provider -> `cjk_name_strokes` or school-specific onomancy engine.

The existing `name_numerology` and `chaldean_numerology` modules should remain Latin A-Z tradition engines. Their current embedded letter tables can be extracted later into reusable value systems without changing their public reading contract. A future compatibility option can add accent folding, but only as an explicit option.

### Explicit Tradition Engines

Each script-native reading tradition should still have its own import path and public engine when it becomes a fortune-telling surface:

- `fortune_telling_core.traditions.hebrew_gematria`
- `fortune_telling_core.traditions.arabic_abjad`
- `fortune_telling_core.traditions.greek_isopsephy`
- `fortune_telling_core.traditions.cjk_name_strokes`

Those engines should delegate normalization and numeric value traces to value systems rather than duplicating table logic inline when the table is reusable.

### No Silent Loss

New value systems and engines should reject unsupported meaningful characters instead of ignoring them. Ignoring separators, whitespace, punctuation, and script-specific marks can be allowed when documented and recorded.

The existing `name_numerology` and `chaldean_numerology` engines are compatibility exceptions. They currently ignore characters outside ASCII A-Z after case folding. Preserve that default behavior until a major release. Strict Latin validation should be available only behind an explicit normalization or validation option, such as `normalization=strict_ascii_reject`, and should be recorded in `Selection.modifiers` and `Provenance.notes`.

Examples:

- Hebrew niqqud may be ignored by default if the engine records `vowels=ignored`.
- Arabic harakat may be ignored by default if the engine records `diacritics=ignored`.
- Greek tonos and breathings may be stripped if the engine records `diacritics=stripped`.
- Latin accent folding should be opt-in and recorded as `normalization=latin-accent-fold`.

### Replay Artifact

Replay state belongs in `Selection.modifiers`. `Draw` has no modifiers field; it only records `deck_id`, `spread_id`, and ordered `selections`. A tradition engine must stamp the normalized name, value-system id/version, total, reduced value if any, and per-letter or per-character values into one or more selections so replay can rebuild `Reading.summary` without recalculating from external data.

For single-selection engines, the only selection should carry the complete trace.

For multi-selection engines, use a documented placement strategy:

- Small common traces can be duplicated across every selection as `common` modifiers, matching the current `name_numerology` pattern where expression, soul urge, personality, and `y_mode` are stamped on each selection.
- Larger traces should live on a canonical aggregate selection, usually `total`; sibling selections should include enough local modifiers for their position plus a pointer such as `trace_position=total`.

CJK five-grid output should use the second strategy by default: the `total` selection carries `characters=...`, `stroke_source=...`, `character_set=...`, and the full resolved stroke trace; heaven, person, earth, and outer selections carry their own grid value plus `trace_position=total`.

For small alphabetic systems, per-character values can fit in modifiers as a compact string:

```text
values=י:10,ו:6,ח:8,נ:50
```

For larger CJK stroke systems, modifiers should stamp the resolved characters and stroke counts:

```text
characters=山:3,田:5,太:4,郎:9
```

### Deck and Symbol Strategy

`Selection.symbol_id` must reference a symbol in the active finite `Deck`. Existing decks are enumerable, and the core validates replay against that deck. Raw gematria, Abjad, and isopsephy totals are unbounded, so those totals must not be modeled as one deck symbol per possible number.

Use small fixed structural decks:

- Raw-total engines use one generic result symbol, such as `hebrew_gematria.result.total`, with the actual numeric total in `Selection.modifiers["total"]` and `Selection.modifiers["value"]`.
- Reducing variants can use a finite root deck, such as roots 1-9, with the raw total still stamped in modifiers.
- Engines that expose both raw totals and reduced roots can use a small multi-position spread, for example `total` plus `root`.

This mirrors the existing Chaldean pattern: the deck contains finite root-number symbols, while the raw name total is stored in `Selection.modifiers["total"]`.

## Proposed Common Shape

Each lower-layer value system should expose:

- `id`: Stable id, such as `latin_pythagorean.v1` or `hebrew_gematria.standard.v1`.
- `version`: Calculation table version.
- `normalize(...)`: Input normalization and validation.
- `values(...)`: Per-unit numeric values.
- Optional `sum(...)`: Convenience total over the value trace.

Each tradition engine should expose:

- A finite deck of structural result symbols or enumerable roots.
- A single-position or small multi-position spread.
- `cast(request)` for deterministic computation.
- `draw(request, rng)` for protocol compatibility, ignoring `rng`.

Common request input:

- `name`: Required string.
- Optional system-specific options such as `variant`, `reduction_method`, `final_letter_mode`, or `stroke_source`.

Common stamped modifiers:

- `input_name`: Original input after leading/trailing whitespace normalization.
- `normalized_name`: Name after engine-specific normalization.
- `system`: Stable tradition engine or reading-system id.
- `value_system`: Stable lower-layer value-system id.
- `value_system_version`: Lower-layer value-system version.
- `variant`: Variant table or calculation method.
- `total`: Raw total when applicable.
- `value`: Final number or root.
- `values`: Compact per-character value trace.
- `trace_position`: For multi-selection spreads where a large trace is stored on one aggregate selection.

Common provenance notes:

- `system=...`
- `value_system=...`
- `normalization=...`
- `variant=...`
- Any disputed option, such as `final_letters=standard` or `abjad_order=common`.

## Candidate Systems

### Hebrew Gematria

Module: `traditions/hebrew_gematria`

Lower-layer value systems:

- Hebrew letters receive standard values 1-400.
- Final forms can either share the base value or use `mispar_gadol` values 500-900.

Value-system options:

- `final_letter_mode`: `standard` by default; `gadol` as an explicit option.
- `vowels`: `ignored` by default.

Validation:

- Accept Hebrew letters and final forms.
- Ignore whitespace and punctuation.
- Reject Latin transliterations unless a future separate transliterated-Hebrew engine is designed.

Output:

- `total`: Sum of letter values.
- `small_value`: Optional digit-sum reduction for methods that need it.
- `value`: For the first implementation, use a generic total symbol and stamp the raw total in modifiers, because gematria often compares totals rather than reducing to 1-9.

### Arabic Abjad

Module: `traditions/arabic_abjad`

Lower-layer value system:

- Arabic letters receive Abjad values 1-1000.
- Persian letters can map to their base Arabic values only when `extension=persian`.

Value-system options:

- `order`: `common` by default; `maghrebi` as an explicit option.
- `extension`: `arabic` by default; `persian` later if the table is included.
- `diacritics`: `ignored` by default.

Validation:

- Normalize Arabic presentation forms to base code points.
- Ignore tatweel, harakat, whitespace, and punctuation.
- Reject unsupported letters unless an extension explicitly defines them.

Output:

- Raw `total` is the primary result.
- Optional reduced root can be added only if a documented Abjad divination convention needs it.
- Use a generic finite total symbol for raw totals; do not enumerate possible Abjad totals as deck symbols.

### Greek Isopsephy

Module: `traditions/greek_isopsephy`

Lower-layer value system:

- Greek alphabetic numerals: units, tens, hundreds.
- Include obsolete letters digamma/stigma, qoppa, and sampi for 6, 90, and 900.

Value-system options:

- `era`: `classical` by default.
- `diacritics`: `stripped` by default.
- `sigma_mode`: normalize final sigma to sigma by default.

Validation:

- Accept Greek letters in upper or lower case.
- Strip Greek diacritics when configured.
- Reject Latin transliterations.

Output:

- Raw `total` is the primary result.
- Optional digit reduction should be a separate option, not the default.
- Use a generic finite total symbol for raw totals; do not enumerate possible isopsephy totals as deck symbols.

### Old Cyrillic / Church Slavonic Numerals

Module: `traditions/cyrillic_slavonic_numerals`

This is an isopsephy/gematria-style raw-total system, not a modern Slavic alphabet-position system. Old Cyrillic letters used as numerals borrowed their values from Greek alphabetic numerals and were marked with a titlo when used as numbers [Cyrillic numerals](https://en.wikipedia.org/wiki/Cyrillic_numerals), [Titlo](https://en.wikipedia.org/wiki/Titlo). The system is suitable for Church Slavonic or historical-text use cases only when the input spelling and letter table are explicit.

Lower-layer value system:

- `fortune_telling_core.traditions._name_values.cyrillic_slavonic_numerals`
- Units: `а=1`, `в=2`, `г=3`, `д=4`, `є/е=5`, `ѕ=6`, `з=7`, `и=8`, `ѳ=9`.
- Tens: `і=10`, `к=20`, `л=30`, `м=40`, `н=50`, `ѯ=60`, `о=70`, `п=80`, `ч=90` by the common post-koppa convention.
- Hundreds: `р=100`, `с=200`, `т=300`, `у/ѵ/ꙋ=400`, `ф=500`, `х=600`, `ѱ=700`, `ѡ=800`, `ц=900` by the common table.
- Explicit obsolete or extra letters: `ѕ=6`, `ѳ=9`, `і=10`, `ѯ=60`, `ѵ=400`, `ѱ=700`, `ѡ=800`; `ѣ` has no standard numeric value in the usual early Cyrillic numeral table and should be rejected unless a named variant table defines it [Early Cyrillic alphabet](https://en.wikipedia.org/wiki/Early_Cyrillic_alphabet).

Value-system options:

- `letter_table`: `common_church_slavonic` by default.
- `koppa_mode`: `cherv_90` by default; `koppa_90` for tables that use `ҁ=90`.
- `xi_mode`: `ksi_60` by default; `cherv_60` for Western Cyrillic variants where `ч=60` and `ҁ=90`.
- `u_400_mode`: `uk` by default; `izhitsa` or `both` when `ѵ` is accepted as 400.
- `omega_800_mode`: `omega` by default; `ot` or `broad_omega` only when explicitly supported.
- `unvalued_letters`: `reject` by default. Do not silently drop letters such as `ѣ`, `ж`, `ш`, `щ`, `ъ`, or `ь`.
- `titlo`: `optional` for name analysis; `required` only if a future parser is interpreting mixed prose with embedded numerals.

Validation:

- Accept only letters defined by the selected `letter_table`.
- Strip titlo and Church Slavonic combining marks only when the selected option says they are orthographic markers, not value-bearing characters.
- Reject modern Cyrillic letters, Latin transliterations, and obsolete Cyrillic letters with no value unless a selected variant explicitly defines them.
- Record `letter_table`, `koppa_mode`, `xi_mode`, `u_400_mode`, `omega_800_mode`, `unvalued_letters`, and `titlo` in `Selection.modifiers` and `Provenance.notes`.

Output:

- Raw `total` is the primary result.
- Optional digit reduction should be a separate option, not the default.
- Use a generic finite total symbol for raw totals; do not enumerate possible Old Cyrillic totals as deck symbols.
- Stamp the normalized Cyrillic name and compact value trace in modifiers, for example `values=а:1,р:100,і:10`.

### Modern Cyrillic Pythagorean Numerology

Module: `traditions/cyrillic_pythagorean`

This is a modern alphabet-position 1-9 system, analogous to the existing Latin Pythagorean engine, not a continuation of Church Slavonic numerals. For Russian, the default table should use the modern 33-letter alphabet order, which includes `ё`, `й`, `ъ`, and `ь` [Russian alphabet](https://en.wikipedia.org/wiki/Russian_alphabet).

Lower-layer value system:

- `fortune_telling_core.traditions._name_values.cyrillic_pythagorean`
- Russian 33-letter default: assign values by alphabet position modulo 9 over `а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я`.
- Example Russian 33-letter mapping: `а=1`, `б=2`, `в=3`, `г=4`, `д=5`, `е=6`, `ё=7`, `ж=8`, `з=9`, then cycle so `и=1`, `й=2`, and so on through `я=6`.

Value-system options:

- `language`: `russian` by default; future explicit values can include `ukrainian`, `serbian`, `bulgarian`, or another named Cyrillic alphabet.
- `alphabet`: `russian_33` by default. A `russian_32_no_yo` table is a separate explicit option, not an implicit fallback.
- `yo_mode`: `distinct` by default for Russian 33-letter mode; `fold_to_e` only when explicitly selected and recorded.
- `signs_mode`: `count` by default for Russian 33-letter mode; `ignore_hard_soft_signs` only when explicitly selected and recorded.
- `short_i_mode`: `distinct` by default; any `й -> и` folding must be explicit and recorded.
- `normalization`: `strict_cyrillic` by default, with no silent transliteration from Latin.

Validation:

- Accept letters from the selected Cyrillic alphabet in upper or lower case.
- Reject unsupported letters rather than silently dropping them.
- Reject `ё` when the selected alphabet lacks `ё`, unless `yo_mode=fold_to_e` is selected.
- Reject `й`, `ъ`, or `ь` when the selected policy excludes them, unless the selected folding or ignore option explicitly defines the behavior.
- Record `language`, `alphabet`, `yo_mode`, `signs_mode`, `short_i_mode`, and `normalization` in `Selection.modifiers` and `Provenance.notes`.

Output:

- Same shape as Latin Pythagorean name numerology: expression-style totals and reduced roots can be supported where the tradition engine defines them.
- The deck remains finite and root-based, such as roots 1-9, with raw totals stamped in modifiers.
- Per-letter values should be stamped as a compact trace, for example `values=а:1,л:4,е:6,к:3,с:1,е:6,й:2`.

### CJK Name Stroke Onomancy

Module: `fortune_telling_core.traditions.cjk_name_strokes`

This system is materially different from alphabetic numerology. It depends on written characters and stroke counts, not phonetic spelling. Japanese `seimei handan` and Chinese `xingmingxue` also differ in grid formulas and stroke-count conventions.

Lower-layer provider:

- A `StrokeCountProvider` resolves characters to counts under an explicit character set and source.
- The first provider should be request-supplied counts, not bundled data.

Tradition engine:

- A school-specific engine consumes the stroke provider and computes grid values such as heaven, person, earth, outer, and total.

First implementation should be conservative:

- Accept explicit characters in `surname` and `given_name`, or a full `name` plus explicit split options.
- Require a stroke-count source or provider.
- Support one documented grid formula at a time.

Options:

- `school`: `japanese_seimei_handan` or `chinese_xingmingxue`, not both in one default.
- `character_set`: `traditional`, `simplified`, `shinjitai`, or `kyujitai`.
- `stroke_source`: `request` for the first provider.
- `grid`: `five_grid` by default when the selected school supports it.

Request-supplied stroke counts:

```python
ReadingRequest(
    options={
        "surname": "山田",
        "given_name": "太郎",
        "strokes": "山:3,田:5,太:4,郎:9",
    },
)
```

This avoids shipping a large stroke-count table before licensing and variant policy are settled.

Output:

- Multiple selections can represent grid values such as heaven, person, earth, outer, and total.
- The `total` selection should stamp each character and resolved stroke count; other grid selections should stamp their own value and `trace_position=total`.
- Provenance must record `stroke_source=request`, `character_set=...`, and `school=...`.

#### Candidate Stroke-Count Sources

The stroke source is a school-policy boundary, not a generic data lookup. Japanese `seimei handan` (姓名判断) sources document that five-grid readings are usually based on name character stroke counts, but that schools differ: some count old forms using the Kangxi dictionary (康熙字典), some count current shinjitai, some restore radicals to their full forms, and some disagree on radicals such as `艹` [Japanese Wikipedia, 姓名判断](https://ja.wikipedia.org/wiki/%E5%A7%93%E5%90%8D%E5%88%A4%E6%96%AD). Chinese descriptions of radicals also note the name-divination practice of counting radicals by the original component rather than by the printed form [Chinese Wikipedia, 偏旁](https://zh.wikipedia.org/wiki/%E5%81%8F%E6%97%81). The design should therefore treat `stroke_source` as replay-critical input.

Recommended source classes:

| Source class | Tradition or school served | Stroke-count convention | Character-set basis | Provenance/source type | Licensing and bundling suitability | Variant handling |
| --- | --- | --- | --- | --- | --- | --- |
| Request-supplied counts | Japanese `seimei handan` and Chinese `xingmingxue`; any sub-school when the caller supplies the policy | Caller-declared. Can represent Kangxi strokes, modern shinjitai, simplified strokes, school tables, or special radical rules | Caller-declared per request | Request data, optionally with a source label such as `client_table:v1` | Safe-to-bundle because no dataset is bundled. The caller owns licensing responsibility | Best replay story when each input character has an explicit count and optional `variant` label |
| Injectable provider | Japanese or Chinese engines where an application owns a licensed table | Provider-declared. The provider id must state whether it uses Kangxi, shinjitai, simplified, traditional, or custom rules | Provider-declared | External `StrokeCountProvider` implementation | Injectable-only by default. Bundling suitability belongs to the provider | Provider should return count, source id, source version, and any variant key used |
| Kangxi dictionary or Kangxi-style school table | Old-form Japanese `seimei handan`; traditional Chinese `xingmingxue` (姓名学) schools that use Kangxi strokes | Kangxi dictionary strokes, commonly with radical restoration. Examples: `氵` is counted as `水` with 4 strokes; `艹` may be counted as 3, 4, or 6 depending on school; `阝` must distinguish left `阜` from right `邑` | Kangxi, kyujitai, or traditional Han | Dictionary-derived or school-specific table. Unicode exposes Kangxi dictionary indices such as `kKangXi`, but a school table still needs explicit counting policy [Unicode UAX #38](https://www.unicode.org/reports/tr38/) | Injectable-only or needs-legal-review. Original Kangxi text is historical, but modern digitizations and school tables are often proprietary or licence-uncertain | Code point alone can be insufficient where modern and old forms share display expectations. Provider must identify the normalized form or variant form used |
| Modern Japanese kanji tables | Shinjitai-counting `seimei handan` sub-schools and non-divinatory Japanese stroke lookup | Literal modern printed strokes, not Kangxi radical restoration unless the table says so | Shinjitai/JIS/Joyo/Jinmeiyo-oriented Japanese glyphs | Dictionary table or stroke-order vector dataset such as KANJIDIC2 or KanjiVG | Injectable-only or needs-legal-review. KANJIDIC2 is under EDRDG's CC BY-SA 4.0 dictionary licence [EDRDG licence](https://www.edrdg.org/edrdg/licence.html). KanjiVG is CC BY-SA 3.0 [KanjiVG licence](https://kanjivg.tagaini.net/) | Usually keys by Unicode code point and Japanese glyph convention. It does not resolve all kyujitai/shinjitai policy questions without explicit variant metadata |
| Unicode Unihan `kTotalStrokes` and `kAlternateTotalStrokes` | Generic CJK stroke provider; not a complete `seimei handan` or `xingmingxue` school source by itself | Representative glyph total strokes. `kAlternateTotalStrokes` can carry alternate counts tagged by IRG source; it is not exhaustive [Unicode UAX #38](https://www.unicode.org/reports/tr38/) | Unicode Han repertoire with IRG source metadata | Unicode data file | Safe-to-bundle legally under the Unicode License v3 for data files [Unicode license](https://www.unicode.org/license.txt), but not recommended as the first core bundle because it is not tradition-specific | Handles some source-specific alternate counts through IRG source specifiers and Unicode variant properties, but does not encode school rules such as radical restoration for `seimei handan` |
| Mainland simplified stroke standards | Mainland Chinese modern-name analysis sub-schools that explicitly use simplified or modern literal strokes | Modern simplified regular-script stroke number and stroke order, not Kangxi/traditional counts | Simplified Han and GB/Unicode character sets | National standard tables such as GB13000.1 stroke order/count data, or dictionary-derived tables | Injectable-only unless a redistributable source is identified; otherwise needs-legal-review | Can be precise for simplified code points; traditional/simplified equivalence must be handled outside the count lookup |
| PRC stroke-order graphics datasets | Modern Chinese educational or handwriting support; only indirectly useful for `xingmingxue` if the school accepts modern literal strokes | Computed as the number of SVG/path strokes in a graphics record | Simplified and some traditional Han, usually based on a particular font or PRC stroke order | Computed from stroke-order graphics, such as Make Me a Hanzi or Hanzi Writer data | Injectable-only or needs-legal-review. Make Me a Hanzi derives dictionary data from Unihan/CJKlib and graphics from Arphic fonts [Make Me a Hanzi](https://github.com/skishore/makemeahanzi). Hanzi Writer data is derived from Make Me a Hanzi and distributed under the Arphic Public License [Hanzi Writer data](https://github.com/chanind/hanzi-writer-data) | Variant handling follows the dataset's glyph source and font choices, not a name-divination school |
| School-specific commercial tables | Named `seimei handan` or `xingmingxue` lineages with proprietary conventions | Whatever the school publishes, including radical restoration, special kana counts, old/new form choices, and 81-number handling | School-defined | Proprietary or private table | Needs-legal-review. Do not bundle unless rights are explicit and compatible | Potentially best school fidelity, but provider must expose source id, version, and conflict policy |

Design implication:

- Keep `stroke_source=request` as the first implementation path.
- Allow future values such as `provider:<id>`, `unicode_unihan_kTotalStrokes`, `kangxi_table:<id>`, or `school_table:<id>` only when the source is explicit and replayable.
- Record the selected source, character-set basis, and convention in `Provenance.notes`, and stamp the resolved per-character counts in `Selection.modifiers`.
- Do not treat Unicode or modern stroke-order graphics as equivalent to a Kangxi or school-specific source.

### Indic Kaṭapayādi

Kaṭapayādi is an alphasyllabic numeric encoding system, not a direct drop-in equivalent to Pythagorean name numerology. It is best treated first as a value system, not a fortune-telling engine, unless a clear divination use case is specified.

Potential value-system module:

- `fortune_telling_core.traditions._name_values.katapayadi`

Potential first scope:

- Encode a Sanskrit or Malayalam word to digits.
- Record script normalization and conjunct handling.
- Avoid claiming a fortune-telling interpretation until the tradition-specific reading layer is designed.

## Latin Accent Folding

A smaller compatibility improvement can be added to the Latin value systems and exposed by existing Latin engines:

- Keep current behavior as `normalization=latin_ascii_ignore`, meaning case-fold to A-Z and ignore unsupported non-A-Z characters.
- Add `normalization=latin_accent_fold` option.
- Implement with Unicode NFKD decomposition and removal of combining marks.
- Reject letters that still do not map to A-Z after folding.
- Add strict rejection only as an explicit option until a major release. The default Latin engines should continue ignoring unsupported non-A-Z characters for backward compatibility.

Examples:

- `Jose` and `José` can match under `latin_accent_fold`.
- `Soren` and `Søren` should not be assumed equivalent unless the fold table explicitly maps `Ø -> O`.
- `Łukasz` should require an explicit extended fold table or reject.

This option should be documented as a convenience for Latin-script names, not as script-native numerology.

## Shared Implementation Utilities

Shared helpers can live under a private module such as `traditions/_name_text.py`:

- Unicode normalization wrappers.
- Diacritic stripping.
- Punctuation and separator filtering.
- Compact value-trace formatting and parsing.

Reusable value systems can live under a private namespace such as `traditions/_name_values/` until more than one public engine needs them. Do not place cultural tables or script-specific rules in a generic shared primitive. Keep those inside a named value-system module that owns the convention.

## Testing Plan

For each alphabetic value system:

- Validate known letter-value anchors.
- Validate case or final-form normalization.
- Validate diacritic handling.
- Validate rejection of unsupported letters.
- Validate normalized value traces and totals.
- Validate value-system id/version and variant choices.

For each tradition engine:

- Validate `cast`, replay, and JSON round trip.
- Validate modifiers stamp both `system` and `value_system`.
- Validate provenance notes include tradition and value-system choices.

For CJK stroke onomancy:

- Validate request-supplied stroke-provider parsing.
- Validate name splitting.
- Validate chosen grid formulas with small hand-computed examples.
- Validate character and stroke traces are stamped into the `total` selection modifiers and that sibling selections point to it with `trace_position=total`.
- Validate replay and JSON round trip.

For Latin accent folding:

- Validate default Latin A-Z ignore behavior remains unchanged.
- Validate opt-in folded names match expected A-Z values.
- Validate unsupported folds raise `ValidationError`.
- Validate provenance records the normalization option and value-system id.

## Documentation Plan

- Update `README.md` and `docs/index.md` so included traditions list all shipped engines.
- Add one MkDocs page per new tradition module.
- Clearly document that non-ASCII names are not handled by generic transliteration.
- Document each engine's normalization, value-system id, and variant defaults.
- Include examples using native-script input.

## Migration Plan

1. Document the current Latin A-Z scope for `name_numerology` and `chaldean_numerology`, including that `name_numerology.compute_chart` needs at least one letter, at least one vowel under the selected `YMode`, and at least one consonant for Expression, Soul Urge, and Personality.
2. Extract the current Pythagorean and Chaldean letter tables into private Latin value-system modules without changing public behavior.
3. Add strict validation only behind an explicit Latin normalization or validation option. Do not make strict rejection the Latin default until a major release.
4. Add optional Latin accent folding only if needed for compatibility.
5. Implement Hebrew gematria, Arabic Abjad, and Greek isopsephy value systems first because their tables are compact and dependency-free.
6. Add public tradition engines over those value systems only where the reading contract is clear.
7. Implement CJK stroke onomancy behind request-supplied stroke counts or a provider before considering bundled stroke data.
8. Revisit Kaṭapayādi after the desired divination contract is clear.

## Open Questions and Recommendations

- Raw-total deck strategy: use small structural decks and store actual totals in modifiers. Do not enumerate unbounded totals as deck symbols.
- Latin strict rejection: preserve current ignore behavior by default until a major release. Offer strict rejection only as an explicit option before then.
- Value-system API visibility: keep value systems private until at least two public engines share one and a stable calculator API is justified.
- CJK stroke data: do not bundle school stroke-count data in core. Use request-supplied counts or an injectable provider because stroke sources and character variants carry licensing and school-policy risk. Unicode data may be legally redistributable, but it should still be an explicit generic source, not the default school source.
- Raw-total summaries: keep `Reading.summary` structural only, such as total and optionally compact value trace. Do not add interpretive meaning text; interpretation belongs in the sibling interpreter package.
