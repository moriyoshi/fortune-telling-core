# Celtic Tree Calendar

A Celtic tree calendar (Ogham tree zodiac) engine that deterministically classifies a birth date into
one of thirteen tree signs by fixed date ranges. The scheme is Robert Graves' 20th-century
reconstruction, not an attested ancient calendar; Graves' nameless day (23 December) is folded into
Ruis (Elder).

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.celtic_tree import (
    CELTIC_TREE_DECK,
    CELTIC_TREE_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=CELTIC_TREE_DECK.id,
    spread_id=CELTIC_TREE_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1990-07-01T00:00:00+00:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.celtic_tree
