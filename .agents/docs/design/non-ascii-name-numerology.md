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

> **Excluded — do not implement.** The Arabic Abjad engine is intentionally not
> shipped on cultural-sensitivity grounds: Abjad numerology is an
> Arabic/Islamic-associated divination system, and fortune-telling carries a
> strongly condemning religious context for Muslim audiences. The
> implementation that briefly existed on the `name-value-systems` branch was
> removed for this reason (the same rationale that dropped the `ur-IN` locale in
> the interpreter package). The notes below are retained only to record the
> original proposal. Do not re-add this engine without an explicit decision to
> reverse this policy.

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
