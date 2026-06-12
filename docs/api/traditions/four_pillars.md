# Four Pillars of Destiny (BaZi)

A BaZi engine computing the four natal pillars (eight characters), Ten Gods and five-element
analysis, luck pillars (大运) and the annual pillar, with a selectable time model.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.four_pillars import (
    FOUR_PILLARS_DECK,
    FOUR_PILLARS_SPREAD,
    build_engine,
)

engine = build_engine()
request = ReadingRequest(
    deck_id=FOUR_PILLARS_DECK.id,
    spread_id=FOUR_PILLARS_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={
            "birth_datetime": "1990-01-01T12:00:00+00:00",
            "latitude": "51.5074",
            "longitude": "-0.1278",
            "gender": "male",
            "target_year": "2026",
        },
    ),
)

reading = engine.cast(request)
```

::: fortune_telling_core.traditions.four_pillars
