# Pythagorean Numerology

A Pythagorean numerology engine that deterministically reduces a querent's birth date to a Life Path
and Birthday number. The Life Path reduction method is a configurable option because the two common
methods diverge on master numbers (11, 22, 33).

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.numerology import (
    NUMEROLOGY_DECK,
    NUMEROLOGY_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=NUMEROLOGY_DECK.id,
    spread_id=NUMEROLOGY_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1987-08-17T00:00:00+00:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.numerology
