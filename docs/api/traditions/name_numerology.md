# Name Numerology

A Pythagorean name-numerology engine that deterministically reduces a name to its Expression, Soul
Urge, and Personality numbers. Whether Y counts as a vowel is a configurable option.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.name_numerology import (
    NAME_NUMEROLOGY_DECK,
    NAME_NUMEROLOGY_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=NAME_NUMEROLOGY_DECK.id,
    spread_id=NAME_NUMEROLOGY_SPREAD.id,
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "John"}),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.name_numerology
