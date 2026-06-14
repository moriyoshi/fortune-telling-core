# Supported Traditions — Reference Addendum

This addendum to the product documentation gives, for each fortune-telling
tradition shipped by `fortune-telling-core`, a short factual background (origin,
mechanic, and what it is traditionally used for) and a note on how the library
models it. It complements the per-module [API Reference](api/traditions/tarot.md);
it does not replace it.

The library implements **22 traditions**. Arabic **Abjad** numerology is
deliberately *not* shipped (see [Cultural and religious context](#cultural-and-religious-context)).

---

## Cultural and religious context

**Please read this section first.**

The systems documented here are **cultural, religious, and folk belief
traditions** drawn from many societies and spanning more than three thousand
years. This reference — and the library — presents them **descriptively and
respectfully**. Including a tradition is **not an endorsement** of its claims,
and the library makes **no claim of predictive or scientific validity**. The
engines compute *structural* artifacts (numbers, symbols, calendar positions);
they do not assert that those artifacts are true of any person or event.

Several points deserve explicit care, because mishandling them can cause real
offense:

- **Living and sacred traditions.** Some of these are not historical
  curiosities but practices that communities hold sacred today — for example the
  Maya **Tzolk'in** day-count is still kept by traditional Maya communities, and
  the **I Ching** and **Four Pillars** are rooted in living Chinese cosmology.
  Present them as the cultural property of those communities, not as novelties.
- **Primarily religious, only secondarily "fortune-telling."** **Hebrew
  gematria**, **Greek isopsephy**, and the **Cyrillic / Church Slavonic**
  numeral tradition are first and foremost *religious and scriptural*
  hermeneutic practices — central to Kabbalah, to Jewish and Christian exegesis,
  and to Orthodox liturgical culture. They are only loosely, and often
  anachronistically, grouped with popular divination. Describe them in their
  religious terms; do not reduce them to "name fortune-telling."
- **Sensitivity can warrant exclusion.** Where divination carries a *strongly
  condemning* religious context for a community, the library declines to ship a
  system rather than risk offense. **Arabic Abjad numerology is excluded** on
  these grounds (fortune-telling is widely condemned in Islam, and Abjad is an
  Arabic/Islamic-associated system); for the same reason the interpretation
  package omits the Urdu (`ur-IN`) locale. These are intentional product
  decisions, not oversights.
- **Authenticity vs. popular myth.** Some widely marketed "ancient" systems are
  modern constructions. The **Celtic Tree Calendar** is a 20th-century literary
  invention by Robert Graves (1948), not ancient Celtic lore; modern **rune**
  and **tarot** *divination* are revivals/reinterpretations layered onto an
  authentic older script and card game; and the **Petit Lenormand** was named
  after a fortune-teller who never used it. This document flags such gaps so the
  product does not repeat popular myths as fact.
- **Examples and presentation.** Use neutral, fictional placeholder names in
  examples (e.g. `山田太郎`, `Иван`, common words like `שלום` "peace") — never
  the names of real political, public, or religious figures. When surfacing
  readings to end users, frame them as cultural/symbolic content, not as factual
  prediction or religious endorsement.

A practical convention runs throughout the library: where schools or conventions
genuinely diverge (stroke-counting rules, Y-as-vowel, calendar day boundaries,
gematria finals), the divergence is **surfaced as a configurable option with a
documented default** rather than hardcoded — so a deployment can match the
convention its audience expects.

---

## How the library models a tradition

Every tradition exposes an `Engine` with a **deck** (the pool of possible
symbols) and a **spread** (named positions), and produces a replayable `Draw`
plus a structural `Reading`. Two mechanics are used:

- **Drawn** — the outcome depends on caller-supplied randomness through
  `read(request, rng=...)`; the engine shuffles or casts symbols. Used for
  card/tile/lot systems.
- **Computed (Cast)** — the outcome is *deterministic* from input data through
  `cast(request)`; no randomness is used. Used for birth-data and name-based
  systems.

The core is **structural only**: engines emit numbers, symbols, calendar
positions, and a short factual `summary`. Human-facing interpretive text lives
in the separate interpretation package, not here.

---

## Drawn traditions

### Tarot (Rider–Waite–Smith)

**Background.** Tarot began as a 15th-century northern-Italian card game
(*tarocchi*) and was repurposed for divination in 18th–19th-century France. The
Rider–Waite–Smith deck (London, 1909; A. E. Waite and Pamela Colman Smith of the
Hermetic Order of the Golden Dawn) is the most influential modern deck. It holds
**78 cards**: the **22 Major Arcana** (archetypal themes, 0 The Fool – 21 The
World) and **56 Minor Arcana** in four suits (Wands, Cups, Swords, Pentacles).
Cards are shuffled and laid in a *spread*; a card dealt upside-down (a
**reversal**) may be read with a modified meaning. Used for reflection and
narrative insight rather than literal prediction.

**In the library.** *Drawn.* Deck = 78 RWS cards; spreads = single card and
past/present/future three-card. Optional `allow_reversals` records an upright or
reversed orientation per card.

### Petit Lenormand

**Background.** A **36-card** deck named (posthumously) after the Napoleonic-era
fortune-teller Marie Anne Lenormand, modelled on the c. 1799 parlor game *Das
Spiel der Hoffnung*. Unlike tarot it uses plain everyday symbols (House, Ship,
Ring) with fairly fixed meanings, is **not read reversed**, and is read in
**pairs/lines** where neighbours modify each other; its signature layout is the
**Grand Tableau** of all 36 cards. Favors concrete situational answers.

**In the library.** *Drawn.* Deck = 36 Lenormand cards; spreads = single card,
three-card line, and the 36-position Grand Tableau. No reversals.

### Dominoes (dominomancy)

**Background.** Folk fortune-telling by drawing tiles from a **double-six set of
28 tiles** and reading the pips; doubles and high-pip tiles carry stronger
meaning. Dominoes reached Europe from China in the 18th century; the practice
became associated with Romani fortune-tellers and has no single authoritative
meaning system.

**In the library.** *Drawn.* Deck = the 28 double-six tiles (high/low pips, pip
total, `double` flag); spreads = single tile and past/present/future.

### Elder Futhark runes

**Background.** The Elder Futhark is the oldest runic alphabet (**24 runes**,
c. 2nd–8th c. AD, Germanic Europe), arranged in three groups of eight (*ættir*).
Each rune has a name and meaning by acrophony (e.g. *Fehu* "wealth", *Laguz*
"water"). Historically a writing system on objects and runestones; modern rune
*divination* — drawing rune-marked lots and interpreting them — is largely a
20th-century reconstruction.

**In the library.** *Drawn.* Deck = 24 Elder Futhark runes (keyword, aett);
spreads = single rune and the three Norns (past/present/future). Optional
`allow_reversals` for the non-symmetrical runes.

### Western geomancy

**Background.** A Renaissance divination system that entered Europe from the
Arabic *‘ilm al-raml* ("science of the sand"). It uses **16 geomantic figures**
(four rows of one or two points), each tied to a classical element. A reading
generates four **Mother** figures from random marks, then derives Daughters,
Nieces, two **Witnesses**, and a final **Judge**, arranged in the **Shield**
chart; the Judge gives the overall answer.

**In the library.** *Drawn.* Four Mothers are cast from the RNG and the rest of
the shield is derived deterministically (geomantic addition = bitwise XOR). Deck
= 16 figures; spread = the 15-position shield.

### I Ching (Yijing)

**Background.** The Chinese *Book of Changes* (core text c. 1000–750 BCE). Its
symbols are the eight trigrams, paired into **64 hexagrams** of six lines. A
consultation builds a hexagram line by line (yarrow stalks, or the later
three-coin method); "old" (changing) lines flip, transforming a **primary
hexagram** into a **relating** one, read as movement between situations.
Hexagrams follow the King Wen sequence.

**In the library.** *Drawn.* Each of six lines is cast by a three-coin model;
the engine yields the primary hexagram, the changing-line positions, and the
relating hexagram. Deck = 64 hexagrams; spread = primary + relating.

---

## Computed traditions — astrology and calendars

### Western astrology (natal/tropical)

**Background.** Descended from Hellenistic astrology (Ptolemy's *Tetrabiblos*),
with Babylonian/Egyptian roots. A **natal chart** maps the Sun, Moon, and planets
against the 12 tropical zodiac signs for an exact birth time and place, divided
into 12 houses, oriented by the Ascendant. Interprets signs, planets, houses,
and aspects as personality and life themes. (A claim of symbolic correspondence,
not supported by scientific evidence.)

**In the library.** *Computed* from `birth_datetime`, `latitude`, `longitude`.
Deck = the 12 signs (tropical or sidereal); spread = natal positions
(luminaries, planets, nodes, angles). Configurable zodiac and house system; the
summary lists major aspects.

### Four Pillars of Destiny (BaZi / 四柱推命)

**Background.** A Chinese fate-analysis system (also Korean *Saju*, Japanese
*Shichū Suimei*). The birth **year, month, day, and hour** each become a pair of
one of ten **Heavenly Stems** (a Five-Element phase in yin/yang polarity) and one
of twelve **Earthly Branches** (the zodiac animals) — "eight characters." The
Day Pillar's stem is the "Day Master" (the person); the balance of the Five
Elements describes character and fortune over time.

**In the library.** *Computed* from birth date-time and place. Deck = the 22
stems/branches; spread = the eight pillar slots. Surfaces element balance, Day
Master strength, and luck pillars. Day boundary and time model are configurable.

### Nine Star Ki (九星気学)

**Background.** A Japanese system consolidated by Shinjirō Sonoda (1924) from
Chinese Flying Star feng shui, built on the **Lo Shu** 3×3 magic square. The nine
stars (1–9), each tied to a trigram, element, color, and direction, place a
person by **birth year** (with month/day refinements). Used for temperament and
auspicious timing/direction.

**In the library.** *Computed* from birth date-time. Deck = 9 stars; spread =
principal/monthly/daily/tendency stars, with annual and monthly flying-star
charts.

### Vietnamese Can Chi

**Background.** The Vietnamese name for the East Asian **sexagenary cycle**: ten
Heavenly Stems (*Can*) paired with twelve Earthly Branches (*Chi*, the zodiac
animals — notably the **cat** in place of the rabbit). Yin/yang pairing rules
yield a **60-year cycle**; a year, day, or hour is named stem-then-branch (e.g.
*Giáp Tý*).

**In the library.** *Computed* from birth date-time. Deck = the stems and
branches (with animals); spread = day and hour pillars (stem + branch each).

### Thai Thaksa

**Background.** A Thai astrological framework of Hindu-Buddhist planetary lore
organized by **day of the week of birth**, using **eight** positions because
Wednesday splits into day and (Rahu-ruled) night. Each position carries a
planetary deity, animal, direction, color, and Buddha image; widely used for
character reading and **auspicious naming**.

**In the library.** *Computed* from birth date-time. Deck = the eight grahas;
spread = the eight Thaksa houses; the summary names the ruling graha and the
inauspicious *Kalakini*.

### Javanese Weton

**Background.** Pairs the 7-day week with the indigenous 5-day **pasaran** market
week (Legi, Pahing, Pon, Wage, Kliwon), giving **35** combinations on a 35-day
cycle. Each day carries a *neptu* number; a person's neptu is the sum of the two.
Drawn from the *primbon* tradition; used for personality, compatibility, and
choosing auspicious dates.

**In the library.** *Computed* from birth date-time. Deck = the 7 weekdays and 5
pasaran days (with neptu); spread = saptawara + pancawara; the summary shows the
combined neptu (e.g. "Jumat Legi: neptu 6 + 5 = 11"). Day boundary configurable.

### Celtic tree calendar (Ogham)

**Background.** The **Ogham** script is genuinely ancient (Early-Medieval Irish,
c. 4th–6th c. AD). The popular **tree calendar** that assigns a birth-tree to a
span of the year, however, is a **20th-century construction by Robert Graves**
(*The White Goddess*, 1948), not ancient Celtic lore — a distinction this
reference keeps explicit. Used today for birth-sign-style personality readings.

**In the library.** *Computed* from birth date (fixed Graves date ranges). Deck =
13 tree signs (with Ogham letter and date range); spread = a single birth sign.

### Maya Haab'

**Background.** The Maya 365-day "vague year": **18 months of 20 days + 5
Wayeb' days**, with no leap correction (so it drifts). A date is a day-number
plus month name, each month starting from a "seating" (day 0). Pairs with the
Tzolk'in in the 52-year Calendar Round.

**In the library.** *Computed* from birth date via the GMT correlation. Deck =
the 19 month-periods; spread = a single Haab' date.

### Maya Tzolk'in

**Background.** The Maya 260-day **sacred count**: 13 numbers × 20 day-names,
co-prime so all 260 pairings are unique. The oldest Mesoamerican calendar cycle,
**still kept by traditional Maya communities**; used for divination, naming, and
choosing auspicious days. With the Haab' it forms the Calendar Round (LCM of 260
and 365 = 18,980 days ≈ 52 years).

**In the library.** *Computed* from birth date via the GMT correlation. Deck =
20 day-signs (with trecena number and direction); spread = a single day-sign
(e.g. "4 Ajaw").

---

## Computed traditions — numerology and letter-value systems

> Reminder: the Hebrew, Greek, and Cyrillic systems below are primarily
> **religious and scriptural** traditions; see
> [Cultural and religious context](#cultural-and-religious-context).

### Pythagorean numerology (birth date)

**Background.** The common Western system; the "Pythagorean" name is attributive
rather than literally ancient. From a birth date it derives the **Life Path** and
related numbers by summing digits and **reducing** to 1–9, preserving the
"master numbers" 11/22/33.

**In the library.** *Computed* from birth date. Deck = single digits + master
numbers; spread = Life Path and Birthday. Reduction method configurable.

### Name numerology (Pythagorean)

**Background.** Maps Latin letters A–I=1–9, J–R=1–9, S–Z=1–8, and derives core
numbers from a name: **Expression** (all letters), **Soul Urge** (vowels), and
**Personality** (consonants). The treatment of **Y** (vowel or consonant) is a
genuine ambiguity that changes results.

**In the library.** *Computed* from `name`. Deck = digits + masters; spread =
expression / soul urge / personality. Whether **Y** counts as a vowel is a
documented option (default: consonant).

### Chaldean numerology

**Background.** Named for ancient Babylonia but known mainly through "Cheiro"
(early 20th c.). Letters take values **1–8 only** (9 is held sacred), assigned by
sound rather than alphabetical order; the reduced root carries a **planetary**
ruler (1 Sun, 2 Moon, … 9 Mars).

**In the library.** *Computed* from `name`. Reduces the letter sum to a root 1–9.
Deck = the 9 planetary roots; spread = a single name number; the summary gives
the root, planet, and pre-reduction total.

### Hebrew gematria

**Background.** Assigns the 22 Hebrew letters values 1–400; the **standard**
method (*mispar hechrachi*) gives finals their base values, while *mispar gadol*
gives the five finals 500–900. A famous example is **chai** (חי, "life") = 18.
Primarily a **religious/mystical** practice (Kabbalah, rabbinic exegesis), not
chiefly divination.

**In the library.** *Computed* from a Hebrew `name`. Niqqud are stripped
(recorded as `vowels=ignored`); unsupported characters are rejected. Because
gematria compares raw totals, the engine uses a single structural "total" symbol
and stamps the total in modifiers (summary: "Gematria total 68."). Standard vs.
`gadol` finals is an option.

### Greek isopsephy

**Background.** The Greek counterpart of gematria, summing **Milesian/Ionic**
alphabetic numerals (units, tens, hundreds, with archaic signs digamma=6,
qoppa=90, sampi=900). Famous instances are Christian: **Iēsous** (Jesus) = 888,
set against **666**. Largely a religious, literary, and mystical practice.

**In the library.** *Computed* from a Greek `name`. Diacritics are stripped and
final sigma normalized by default; raw total over a single structural symbol.

### Cyrillic / Church Slavonic numerals

**Background.** An alphabetic numeral system (First Bulgarian Empire, late 10th
c.) modelled on the Greek scheme: Cyrillic letters denote 1–900, marked off from
text by a **titlo**. Standard in Rus' until Peter the Great's reforms; it
persists in **Church Slavonic liturgy** — a religious/liturgical tradition, not a
fortune-telling device.

**In the library.** *Computed* from Old Cyrillic input. Raw total over a single
structural symbol; the several historical letter-form variants (koppa/cherv for
90, ksi for 60, uk/izhitsa for 400, omega for 800) are exposed as options, with
unvalued letters rejected by default.

### Modern Cyrillic (Russian Pythagorean)

**Background.** A contemporary popular adaptation — *not* a continuation of the
medieval numerals — applying a Pythagorean-style position map across the 33-letter
Russian alphabet to a name (the published table: 1=аисъ, 2=бйты … 9=зрщ).

**In the library.** *Computed* from a Cyrillic `name`. Reduces to a root 1–9 over
a root-number deck. Alphabet/language and the handling of ё, й, and the hard/soft
signs are configurable.

### CJK name-stroke onomancy (five-grid)

**Background.** Japanese **seimei-handan** (姓名判断) / Chinese **五格剖象**, the
modern five-grid method created by Kumazaki Kenō (c. 1918–1920s). From the
brush-stroke counts of the name's characters it computes five "grids" — **天**
heaven, **人** person, **地** earth, **外** outer, **総** total — each judged
against an 81-number table. **Schools disagree** on stroke counting (traditional
Kangxi vs. modern forms), so the same name can yield different numbers.

**In the library.** *Computed* from `surname`, `given_name`, and **caller-supplied
stroke counts** (`strokes`, e.g. `山:3,田:5,太:4,郎:9`) — the library bundles no
stroke database (a deliberate licensing/variant decision). Computes the five
grids by the standard 熊崎式 formulas, including the single-character "spirit
number" (霊数) rule; deck/spread = the five grid positions; `school` and
`character_set` are recorded for provenance.

---

## A note on what these engines do and don't claim

Each engine produces a *reproducible structural artifact* and a short factual
`summary`, and records its inputs, options, and normalization choices in
provenance so a reading can be replayed and audited. The engines do **not**
generate interpretive or predictive prose, and the presence of a tradition here
implies neither that its claims are valid nor that the project endorses them. See
[Cultural and religious context](#cultural-and-religious-context) for the
framing this project asks integrators to maintain when surfacing readings to end
users.

---

## Sources

Background in this addendum draws on standard reference material, including the
Wikipedia and Encyclopædia Britannica articles for each tradition (e.g.
*Rider–Waite Tarot*, *Elder Futhark*, *Geomancy*, *I Ching divination*,
*Four Pillars of Destiny*, *Sexagenary cycle*, *Haab'*, *Tzolkʼin*, *Numerology*,
*Gematria*, *Isopsephy*, *Cyrillic numerals*, *Onomancy*), Mesoamericanist and
sinological sources, and — for authenticity caveats — scholarship on the Ogham
script and Robert Graves's *The White Goddess*. Letter-value tables and the CJK
five-grid formulas were independently verified against published worked examples
during implementation.
