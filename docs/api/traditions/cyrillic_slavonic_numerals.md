# Old Cyrillic / Church Slavonic Numerals

An Old Cyrillic numeral engine that deterministically sums the Greek-derived
letter values of a Church Slavonic word (1-900). The raw total is stamped over a
single structural result symbol. Historical letter-form variants (koppa/cherv
for 90, ksi for 60, uk/izhitsa for 400, omega for 800) are configurable, and
letters with no numeral value are rejected by default rather than dropped.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.cyrillic_slavonic_numerals import (
    CYRILLIC_SLAVONIC_NUMERALS_DECK,
    CYRILLIC_SLAVONIC_NUMERALS_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=CYRILLIC_SLAVONIC_NUMERALS_DECK.id,
    spread_id=CYRILLIC_SLAVONIC_NUMERALS_SPREAD.id,
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "миро"}),
)
reading = build_engine().cast(request)
# м=40, и=8, р=100, о=70 -> total 218
```

::: fortune_telling_core.traditions.cyrillic_slavonic_numerals
