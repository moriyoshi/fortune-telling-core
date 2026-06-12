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
