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
