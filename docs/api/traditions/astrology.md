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

::: fortune_telling_core.traditions.astrology
