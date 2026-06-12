# fortune-telling-core

`fortune-telling-core` is a composable, reproducible Python library for building
fortune-telling and divination systems. It provides a small, deterministic, typed core of
primitives - readings, symbols, spreads, draws, structural summaries, and provenance - with
tradition-specific engines layered on top.

## Design principles

- **Deterministic and reproducible.** Randomness enters through one narrow `Rng` protocol, and
  every reading records the exact `Draw` that produced it, so a reading can be replayed without
  any randomness. Computed traditions (astrology, Four Pillars, Nine Star Ki) derive their draw
  from birth data and an injectable `Ephemeris`.
- **Tradition-agnostic core.** The core knows only symbols, positions, selections,
  deterministic summaries, and audit metadata. Each tradition lives behind its own module and
  is never re-exported from the top-level package.
- **Harness-owned interpretation.** The library emits structural readings and deterministic
  summaries. Discretionary meanings, localisation, and presentation copy belong in the
  consuming fortune-telling harness.
- **Configurable where schools diverge.** Where established schools or conventions disagree (house
  systems, zodiac/ayanamsa, time models, the Nine Star Ki day-star escapement), the choice is a
  documented option recorded in each reading's provenance.

## Layout

- **Core** - the tradition-agnostic engine, value types, and serialisation.
- **Astronomy** - shared, tradition-neutral astronomy (Julian day, solar terms, the `Ephemeris`
  protocol and a pure-Python `BuiltinEphemeris`).
- **Traditions** - each exposes an engine plus its deck and spread, imported from its own subpackage.
  Drawn traditions take caller-provided randomness via `read` (`tarot`, `lenormand`, `dominoes`,
  `runes`, `geomancy`, `iching`); computed traditions derive their draw from birth or identity data
  via `cast` (`astrology`, `four_pillars`, `nine_star_ki`, `numerology`, `name_numerology`,
  `chaldean_numerology`, `can_chi`, `thaksa`, `weton`, `celtic_tree`, `haab`, `tzolkin`). See the
  **API Reference** for each.

## Getting started

```python
from fortune_telling_core import RandomRng, ReadingRequest, reading_to_json
from fortune_telling_core.traditions.tarot import RWS_DECK, SINGLE_CARD, build_engine

engine = build_engine()
request = ReadingRequest(
    deck_id=RWS_DECK.id,
    spread_id=SINGLE_CARD.id,
)

reading = engine.read(request, rng=RandomRng(seed=42))
payload = reading_to_json(reading)
```

## Building these docs

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[docs]"
mkdocs serve   # or: mkdocs build
```

See the **API Reference** for the generated documentation of every public symbol.
