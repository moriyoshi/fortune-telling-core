# Astrology

A natal-chart engine: tropical or sidereal zodiac, ten planets plus the lunar nodes and the
Ascendant/Midheaven, Whole Sign / Equal / Placidus houses, and aspects rendered into the summary.
A lightweight [sun-sign spread](#sun-sign) is also available for callers who have only a birthday.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.astrology import NATAL_CHART, TROPICAL_ZODIAC, build_engine

engine = build_engine()
request = ReadingRequest(
    deck_id=TROPICAL_ZODIAC.id,
    spread_id=NATAL_CHART.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={
            "birth_datetime": "1990-01-01T12:00:00+00:00",
            "latitude": "51.5074",
            "longitude": "-0.1278",
            "house_system": "whole_sign",
        },
    ),
)

reading = engine.cast(request)
```

## Sun sign

The `SUN_SIGN` spread is a single-placement reading that needs **only the
querent's zodiac sign** — no birth time, latitude, or longitude — so it serves
callers who know just a birthday. The sign is taken from an explicit `sun_sign`
attribute (a `Sign`, a sign symbol id like `astro.sign.leo`, or a bare slug like
`leo`); when that is absent, a `birth_date` (or `birth_datetime` — only the
calendar date is used) is classified into a sign using the conventional Western
tropical date ranges (`sign_for_date` / `zodiac_date_range`). The placement
reuses the `sun` position id, so the same Sun-in-sign interpretation data
applies as in the natal chart.

Sun-sign readings are always tropical: the conventional date ranges are a
tropical convention, and a sidereal sun sign is not well-defined from a date
alone. The reading touches neither the ephemeris nor birth time and place, and
like the natal chart it is deterministic and replay-safe.

```python
from fortune_telling_core.traditions.astrology import SUN_SIGN, TROPICAL_ZODIAC

reading = engine.cast(
    ReadingRequest(
        deck_id=TROPICAL_ZODIAC.id,
        spread_id=SUN_SIGN.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_date": "1990-04-15"},  # or {"sun_sign": "aries"}
        ),
    )
)
# reading.summary == "Sun sign Aries (fire, cardinal), Mar 21 – Apr 19."
```

## Transits

Set the request's [`as_of`](../core.md#natal-vs-timed-readings) moment to add a
transit report: the engine computes the transiting bodies for that instant and
appends every transit-to-natal aspect (transiting planets against natal planets
and angles) to the summary, under a `Transits as of …` heading. Without `as_of`
the reading is the pure, timeless natal chart. The transit longitudes are stored
on the draw, so replays are ephemeris-free like the natal chart. The transiting
set drops the South Node (the mirror of the North Node) to avoid doubled lines;
aspect orbs are the same defaults used for natal aspects.

### Structured aspects

Aspects are also exposed as **structured data**, not just summary prose, so an
interpretation layer can localize them without recomputing any astronomy. Each
aspect is an entry in `Reading.draw.extras` — a `Selection` with
`symbol_id = "astro.aspect.<type>"` (type ∈ conjunction / opposition / trine /
square / sextile) and modifiers `first`, `second` (body ids), `orb`, and `kind`
(`natal` or `transit`; for a transit, `first` is the transiting body and
`second` the natal body). `extras` are draw selections not bound to a spread
position, so they round-trip through serde and replay like everything else. The
freeform summary is unchanged and always agrees with the structured set.

```python
from datetime import UTC, datetime

reading = engine.cast(
    ReadingRequest(
        deck_id=TROPICAL_ZODIAC.id,
        spread_id=NATAL_CHART.id,
        querent=request.querent,
        as_of=datetime(2026, 6, 16, tzinfo=UTC),  # transits for this moment
    )
)
```

::: fortune_telling_core.traditions.astrology
