# Maya Tzolk'in

A Maya Tzolk'in (260-day sacred round) engine that deterministically derives a querent's Tzolk'in
day — a trecena number (1-13) paired with one of twenty day signs — from their birth date. The cycle
uses the GMT (584283) correlation, anchored at 21 December 2012 = 4 Ajaw.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.tzolkin import TZOLKIN_DECK, TZOLKIN_SPREAD, build_engine

request = ReadingRequest(
    deck_id=TZOLKIN_DECK.id,
    spread_id=TZOLKIN_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "2012-12-21T00:00:00+00:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.tzolkin
