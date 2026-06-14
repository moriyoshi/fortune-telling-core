# Modern Cyrillic Pythagorean Numerology

A modern Russian "Pythagorean-style" numerology engine that reduces a Cyrillic
name to a root number (1-9) using a position map across the 33-letter Russian
alphabet (1=аисъ, 2=бйты … 9=зрщ). The alphabet/language and the handling of ё,
short-i (й), and the hard/soft signs (ъ, ь) are configurable; unsupported
letters are rejected.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.cyrillic_pythagorean import (
    CYRILLIC_PYTHAGOREAN_DECK,
    CYRILLIC_PYTHAGOREAN_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=CYRILLIC_PYTHAGOREAN_DECK.id,
    spread_id=CYRILLIC_PYTHAGOREAN_SPREAD.id,
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "Иван"}),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.cyrillic_pythagorean
