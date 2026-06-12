# Maya Haab'

A Maya Haab' (365-day vague year) engine that deterministically derives a querent's Haab' date — a
day position within a named month — from their birth date. The month deck holds the eighteen winal
plus the five-day Wayeb'. The cycle uses the GMT (584283) correlation, anchored at 21 December
2012 = 3 K'ank'in, and partners the Tzolk'in in the Calendar Round.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.haab import HAAB_DECK, HAAB_SPREAD, build_engine

request = ReadingRequest(
    deck_id=HAAB_DECK.id,
    spread_id=HAAB_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "2012-12-21T00:00:00+00:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.haab
