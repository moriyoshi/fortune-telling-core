# Journal

## 2026-06-15 — Four new Japanese/CJK computed traditions + day-pillar epoch fix

Added four computed traditions plus shared lunisolar astronomy, and fixed a
pre-existing sexagenary day-pillar bug discovered along the way.

### New traditions
- **`sanmeigaku` (算命学)** — body star chart (人体星図): five 十大主星 and three
  十二大従星 from the year/month/day pillars. Reuses `four_pillars` solar-term
  astronomy, sexagenary cycle, and `ten_gods`. Stars are recorded by source
  stem/branch; the spatial 人体星図 cell layout and 初年/中年/晩年 labelling were
  left to interpretation because sources genuinely diverge (and one research
  pass even self-contradicted). 元命 defaults to each branch's 本気 via a
  documented `HiddenStemRule` hook; the day-threshold (月律分野) rule was *not*
  bundled because no authoritative public table was available.
- **`sukuyo` (宿曜)** — birth mansion (本命宿) from the Moon's sidereal ecliptic
  longitude over the 27 mansions. Reuses the bundled Moon ephemeris; ayanamsa
  (Lahiri default / Fagan-Bradley / tropical) is the school-divergence option.
- **`koyomi` (暦注)** — day-quality: 六曜, day 干支, sectional solar month, and
  the 一粒万倍日 / 三隣亡 / 天赦日 select-day flags. 不成就日 (contradictory
  source tables) and the calendrical 二十八宿 (no verifiable epoch anchor) were
  omitted rather than guessed.
- **`zi_wei` (紫微斗数)** — twelve-palace chart with the fourteen major stars:
  命宮/身宮, 五行局 (from 命宮 納音), and the 紫微/天府 series. Minor stars and
  四化 are out of scope (they reference non-major stars and diverge by school).

### Shared infrastructure
- **`astronomy/lunisolar.py`** — dependency-free 旧暦 converter (new-moon finding
  + 中気 month-numbering + leap-month detection, 定気法), built on the existing
  Moon/Sun ephemeris. Validated against known conversions including leap-month
  years (e.g. 2023 閏二月, 2014 閏九月).

### Bug fix (pre-existing)
The sexagenary **day-pillar epoch was off by two days**: code assumed
`1984-02-02 = 甲子`, but that date is authoritatively **丙寅** (verified against
万年暦; 2000-01-07 is a true 甲子 day, the corrected anchor). This made the day —
and hour — 干支 two days early in `four_pillars`, `nine_star_ki` (day-star
escapement), and `can_chi`. Corrected the anchor in all three and updated the
affected tests to the now-correct values. End-to-end check: `koyomi`'s computed
2024 天赦日 (1/1, 3/15, 5/30, 7/29, 8/12, 10/11, 12/26) now match published
calendars, and 2024-01-01 correctly resolves as both 天赦日 and 一粒万倍日.

### Findings / decisions
- LLM/web research on these traditions is unreliable for exact tables: the
  納音五行 table, a worked 紫微 example, the 天府 relationship, and several
  四化/一粒万倍日 rows came back wrong in research passes. Every numeric table
  shipped here was cross-checked against canonical sub-tables (e.g. 起紫微 against
  the 水二局/火六局 day tables; 天府 against the 紫微-天府 reflection table) or
  against published worked dates. Where no authoritative source could be
  verified, the feature was omitted rather than approximated.
- 六星占術 and カタカムナ were deliberately skipped: their authoritative tables are
  proprietary / not cleanly sourceable.

### Postmortem: an unsourced "commonly cited" claim in a code comment

While fixing the day-pillar anchor I wrote a comment calling 1984-02-02 the
"commonly cited" 甲子 day. That provenance claim was never sourced — a web
search backs only that **1984 is a 甲子 *year*** (1924/1984/2044), not that the
date is a widely-used 甲子-*day* anchor. The comment was corrected to state only
verifiable facts (it was this code's previous anchor; 万年暦 lookups show 丙寅;
the year/day conflation is the *likely* origin).

Root cause, honestly:
- **Laundering via an adjacent true fact.** The refutation (1984-02-02 = 丙寅)
  was solidly sourced; "commonly cited" was added as explanatory colour in the
  same sentence and borrowed the verified fact's credibility.
- **Relaying agent output as established fact.** The phrasing traced to a
  research sub-agent's unverified assertion ("many BaZi sources list it as 甲子")
  plus a training-derived prior. Sub-agent output is a *claim*, not a citation.
- **Plausibility from the very bug being explained.** 1984 *is* a 甲子 year, so
  "commonly cited as a 甲子 day" rhymes with the year/day conflation that caused
  the original bug — a false claim shaped like a true one.
- **No verification gate on prose.** Numeric tables were all cross-checked
  against canonical sources (or omitted when unverifiable); that same "verify or
  omit" discipline was not applied to explanatory comments, which no test, type,
  or lint check validates.

Mitigations going forward:
- Hold prose — especially provenance words like "commonly / standard / widely"
  — to the same "cite it or don't claim it" bar as computed values.
- Treat sub-agent claims as unverified until independently sourced; prefer
  stating checkable facts ("this repo's previous anchor", "万年暦 shows 丙寅")
  over editorialising about prevalence.

### Documentation completeness

Adding a tradition touches more than its own package. The first pass updated the
per-tradition API pages (`docs/api/traditions/*.md`), the mkdocs nav, and the
README "Included Systems" list, but missed `docs/traditions-reference.md` — the
prose reference with a Background / In-the-library section per tradition. Added
sections for all four new traditions and corrected the implemented count to 27
(it read "22"; it had in fact been off by one — 23 sections — before this work).
Checklist for the next tradition: package files, tests, `docs/api/traditions/`,
mkdocs nav, README list, **and** `docs/traditions-reference.md` (+ its count).

### Test hardening (smoke → authoritative)

A review pass replaced self-referential assertions (asserting what the engine
itself emits) with checks against independently-known facts:
- lunisolar — known 旧暦 dates including leap-month years.
- koyomi — real published 最強開運日 (2024-01-01 甲子, 2024-03-15 戊寅, each
  天赦日 + 一粒万倍日) plus rule-level checks against the documented 六曜 / 天赦日 /
  一粒万倍日 / 三隣亡 tables.
- sukuyo — the 13°20′ sidereal partition (longitude → mansion) and Lahiri /
  Fagan-Bradley ayanamsa magnitudes at J2000.
- zi_wei — 起紫微 against the canonical 水二局 / 火六局 day-tables, 五行局 from
  known 納音 elements, 命宮 from the canonical month×hour table, and the
  structural opposites 七殺對天府 / 破軍對天相.
- sanmeigaku — the full 通変星 → 十大主星 mapping and 十二運 長生 anchors.

A useful signal that the checks are real, not tautological: the new Sukuyō
partition test caught a wrong *fixture* I wrote (180° is 角宿, not 氐宿). Open
gap: `zi_wei` and `sanmeigaku` are validated component-by-component against
canonical sub-tables, not against a full external worked chart — a trusted
whole-chart fixture for either would be a worthwhile future addition. Suite:
430 tests, ruff + mypy clean.

## 2026-06-16 — Unified "as of" reference time for timed fortunes

Natal divination is fixed by `birth_datetime`, but users also want fortunes
*for a specific moment* (流年/大運 annual & luck pillars, flying-star charts,
almanac days). That capability already existed in three traditions but through
three incompatible knobs: Four Pillars and Nine Star Ki took a `target_year`
int option, Koyomi took a `target_datetime` string, and Nine Star Ki also had a
build-time `target_year` — with no shared way to ask "give me person X as of
date D".

Added one unified concept rather than a fourth bespoke knob:
- `ReadingRequest.as_of: datetime | None` — the timezone-aware moment a reading
  is computed *for*, with an `effective_at` property that falls back to
  `requested_at`. Serialised only when set (no shape change for existing
  requests) and round-trips through `to_dict`/`from_dict`.
- Four Pillars / Nine Star Ki now default the annual year to `as_of` (via
  `effective_at` / explicit precedence) instead of `requested_at`.
- Koyomi keys its target off the nullable `as_of` so the "missing date raises"
  contract is preserved (it must NOT silently fall back to "now").

Precedence is most-specific-first everywhere: the legacy `target_year` /
`target_datetime` options still win over `as_of`, which wins over engine
build-time defaults, which win over `requested_at`. So `as_of` is a strict
superset — no existing caller behaviour changes when it is unset.

Deliberately did NOT touch the natal-only traditions (Sanmeigaku 大運/年運,
Zi Wei 大限/流年, astrology transits): those are the agreed follow-up — adding
real period engines on top of this shared `as_of` foundation. Suite: 437 tests
(+7), ruff + mypy clean.

## 2026-06-16 — Timed fortune engines: Sanmeigaku 大運/年運, Zi Wei 大限/流年, astrology transits

Built the three timed engines on top of the unified `as_of` foundation, so a
caller can read the same natal subject "as of" any moment. Each reuses
already-validated machinery to keep rule-invention risk low, and stores the
period inputs in the draw so replays stay ephemeris-free.

- **Sanmeigaku** (`periods.py`): 年運 (annual 主星/従星 from the year 干支) is
  always rendered for `effective_at`; 大運 (ten-year luck columns) is added when
  the request supplies `gender`, reusing `four_pillars.luck` (`luck_forward` +
  `luck_pillars`) and the existing 通変星→主星 / 十二運→従星 maps. Start age uses
  the same 節入り÷3 convention as Four Pillars.
- **Zi Wei** (`periods.py`): 流年 (annual 命宮 on the year's 太歲 branch) needs no
  gender; the active 大限 (decade limit) is added with `gender`. Decades start at
  the 五行局 number in 虚歳 (born = 1) and step 順/逆 by the same polarity×gender
  rule (`luck_forward`); the major stars do not move.
- **Astrology**: transits gated on an explicit `as_of` (the natal chart is
  timeless — no `as_of` = unchanged pure natal). Transiting bodies for `as_of`
  are computed and their transit-to-natal aspects appended via a new
  `compute_cross_aspects`. Transit longitudes are stashed as selection modifiers
  (the spread's selection set is fixed, so no extra selections), keeping replay
  ephemeris-free. The South Node (mirror of the North) is dropped from the
  transiting set.

Pattern across all three: legacy `target_year` / `target_datetime` still
override `as_of`; gendered direction is the only new required input, and it is
optional so natal-only behaviour is preserved. Tests anchor to externally fixed
facts (2024 = 甲辰, 2000 = 庚辰, 陰年男 逆行 / 陰年女 順行, 五行局 start ages) plus
pure-function unit tests for each `periods.py` / cross-aspect helper. Suite: 456
tests (+19), ruff + mypy clean.

## 2026-06-16 — Harden timed-engine tests with verified worked examples

Followed the established anchoring discipline (external facts + canonical
sub-tables, not self-referential assertions) for the new timed features:

- **Sanmeigaku** `test_periods.py`: 年運 worked across four consecutive
  externally-fixed years (2023癸卯 … 2026丙午) with full 干支 + 主星 + 従星 each
  derived from the canonical 高尾 tables, plus the complete 大運 干支 ladder
  asserted in both 順行 / 逆行 directions (pure sexagenary stepping).
- **Zi Wei** `test_periods.py`: built on the canonical reference chart
  (命宮 亥, 土五局) that `test_chart.py` already validates; 流年 asserted against
  the 太歲 branch for four fixed years, and the full 大限 ladder (ages + branch
  walk + palace/star content) for both directions.
- **Astrology** `test_transits.py`: replaced the single conjunction check with an
  exact orb table covering every aspect type at its inclusive boundary (8/4/6)
  and a verified non-aspect, plus a `_TwoTimeEphemeris` integration test that
  proves transit positions are taken at `as_of` (not birth) — a moved transit
  Sun yields a partile square to natal Sun, which a birth-time bug could not
  produce.

The earlier honest-limitation note still stands: these are component-wise worked
examples anchored to calendar facts and canonical sub-tables, not whole-chart
fixtures from a single trusted published 算命学 / 紫微 source. Suite: 459 tests
(+3), ruff + mypy clean.

## 2026-06-16 — Release intent: v1.0.0 (breaking)

The feat-sanmeigaku branch changes computed output of engines that shipped in
v0.4.0, so the next release is a major bump to **v1.0.0**.

Breaking change (the reason for the major bump): the day-pillar sexagenary anchor
was corrected from 1984-02-02 to 2000-01-07 (the former is 丙寅, not the assumed
甲子 — off by two). This shifts every day pillar / day star / day 干支 produced by
**four_pillars, nine_star_ki, and can_chi** relative to v0.4.0. Charts cast on
v0.4.0 will not match v1.0.0 for these engines.

Everything else on the branch is additive and backward-compatible: the new
sanmeigaku / sukuyo / koyomi / zi_wei engines, the unified `ReadingRequest.as_of`
(optional; legacy `target_year` / `target_datetime` still override), and the
timed-fortune outputs (年運/大運, 流年/大限, transits). No public symbols were
removed or renamed; `build_engine` signatures only gained optional keywords.

Version mechanics: the package version is VCS-tag-derived (`tool.hatch.version
source = "vcs"`), so the authoritative bump is the `v1.0.0` git tag cut on `main`
at release time — a deliberate maintainer step, intentionally NOT done here. The
`__version__` literal in `__init__.py` had been stale at 0.1.0 across the 0.2–0.4
tags. It is now sourced from a generated `_version.py` written by the hatch-vcs
build hook (`[tool.hatch.build.hooks.vcs] version-file`, the documented
write-version-to-file pattern); `__init__` re-exports `__version__` from it, the
file is git-ignored, and `tests/test_package.py` asserts the runtime version
equals the installed distribution metadata instead of pinning a literal. No
version string is hardcoded anywhere, so `__version__` becomes `1.0.0`
automatically once the `v1.0.0` tag is cut.
