# Chaldean Numerology

A Chaldean numerology engine that deterministically reduces a name to its planetary root (1-9) using
the Chaldean letter values (1-8, with nine never assigned to a letter). This is distinct from the
Pythagorean name-numerology tradition.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.chaldean_numerology import (
    CHALDEAN_NUMEROLOGY_DECK,
    CHALDEAN_NUMEROLOGY_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=CHALDEAN_NUMEROLOGY_DECK.id,
    spread_id=CHALDEAN_NUMEROLOGY_SPREAD.id,
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "John"}),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.chaldean_numerology
