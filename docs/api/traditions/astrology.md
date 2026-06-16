# Astrology

A natal-chart engine: tropical or sidereal zodiac, ten planets plus the lunar nodes and the
Ascendant/Midheaven, Whole Sign / Equal / Placidus houses, and aspects rendered into the summary.

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

## Transits

Set the request's [`as_of`](../core.md#natal-vs-timed-readings) moment to add a
transit report: the engine computes the transiting bodies for that instant and
appends every transit-to-natal aspect (transiting planets against natal planets
and angles) to the summary, under a `Transits as of …` heading. Without `as_of`
the reading is the pure, timeless natal chart. The transit longitudes are stored
on the draw, so replays are ephemeris-free like the natal chart. The transiting
set drops the South Node (the mirror of the North Node) to avoid doubled lines;
aspect orbs are the same defaults used for natal aspects.

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
