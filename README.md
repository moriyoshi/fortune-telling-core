# fortune-telling-core

`fortune-telling-core` is a composable, reproducible Python library for building
fortune-telling and divination systems. It provides a small, deterministic, typed core of
primitives for readings, symbols, spreads, draws, structural summaries, and provenance, with
tradition-specific engines layered on top.

## Design Principles

- **Deterministic and reproducible.** Randomness enters through one narrow `Rng` protocol,
  and every reading records the exact `Draw` that produced it. A recorded draw can be
  replayed without any randomness.
- **Tradition-agnostic core.** The core knows only symbols, positions, selections,
  deterministic summaries, and audit metadata. Tradition modules live behind their own
  packages and are not re-exported from the top-level package.
- **Interpretation belongs to harnesses.** Discretionary meanings, localisation, and
  presentation copy are intentionally outside the library. Consumers can map stable
  symbol ids, position ids, modifiers, summaries, and provenance into their own
  interpretation layer.
- **Configurable where schools diverge.** Where established schools or conventions
  disagree, such as house systems, zodiac/ayanamsa, time models, or the Nine Star Ki
  day-star escapement, the choice is a documented option recorded in reading provenance.

## Included Systems

- **Core**: Tradition-neutral value types, engine contracts, replay, serialisation, and
  provenance.
- **Astronomy**: Shared, dependency-free astronomy including Julian-day helpers, solar
  terms, time models, the `Ephemeris` protocol, and a pure-Python `BuiltinEphemeris`.
- **Traditions**: each exposes its engine and deck/spread data from its own subpackage.
  Drawn traditions take caller-provided randomness via `read`:
  `tarot`, `lenormand` (Petit Lenormand), `dominoes`, `runes` (Elder Futhark),
  `geomancy` (Western geomancy), and `iching` (I Ching).
  Computed traditions derive their draw from birth or identity data via `cast`:
  `astrology`, `four_pillars` (BaZi), `nine_star_ki`, `numerology` (Pythagorean),
  `name_numerology`, `chaldean_numerology`, `can_chi` (Vietnamese), `thaksa` (Thai),
  `weton` (Javanese), `celtic_tree` (Ogham tree zodiac), `haab` (Maya Haab'),
  and `tzolkin` (Maya Tzolk'in).

## Quick Start

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

Computed traditions use `cast()` instead of caller-provided randomness:

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.nine_star_ki import (
    NINE_STAR_KI_DECK,
    NINE_STAR_KI_SPREAD,
    build_engine,
)

engine = build_engine()
request = ReadingRequest(
    deck_id=NINE_STAR_KI_DECK.id,
    spread_id=NINE_STAR_KI_SPREAD.id,
    querent=Querent(
        id="example",
        display_name="Example",
        attributes={
            "birth_datetime": "1990-05-17T09:30:00+09:00",
            "latitude": "35.6895",
            "longitude": "139.6917",
        },
    ),
)

reading = engine.cast(request)
```

## Layout

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── src/
│   └── fortune_telling_core/
├── docs/
├── tests/
├── tools/
└── .agents/
    └── docs/
```

## Development

This repository uses a `src/` Python package layout.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

Run the deterministic demo CLI:

```bash
fortune-telling-demo all
fortune-telling-demo tarot --seed 7
fortune-telling-demo nine-star-ki --json --target-year 2026
```

For computed demos, a `--birth-datetime` without a timezone is interpreted in
the terminal timezone and serialized with an offset.

Build or serve the API documentation:

```bash
python -m pip install -e ".[docs]"
mkdocs serve
mkdocs build --strict
```

Regenerate the built-in ephemeris series only when changing source tables or
the truncation threshold. The large public VSOP87D source files are downloaded
into `.cache/ephemeris/vsop87d/`, an ignored local cache outside `tools/`, and
verified by checksum:

```bash
python tools/ephemeris/generate_builtin_series.py --download-missing
python tools/ephemeris/generate_builtin_series.py --check --download-missing
```

Canonical agent-facing project notes live in `.agents/docs/`.

## Licence and Dependencies

`fortune-telling-core` is MIT licensed and is intended to remain zero-copyleft. The required runtime dependency set is empty.

Higher-precision astronomy is bring-your-own through the injectable `Ephemeris` Protocol. Consumers own the licensing review for any ephemeris backend they provide.
