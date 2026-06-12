# Javanese Weton

A Javanese weton (Primbon) engine that deterministically derives a querent's weton (seven saptawara
days paired with five pancawara pasaran) and neptu from their birth datetime.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.weton import WETON_DECK, WETON_SPREAD, build_engine

request = ReadingRequest(
    deck_id=WETON_DECK.id,
    spread_id=WETON_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1945-08-17T10:00:00+07:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.weton
