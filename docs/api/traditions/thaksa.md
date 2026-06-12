# Thai Thaksa

A Thai Thaksa (ทักษา) engine that deterministically seats the eight grahas into a querent's houses
from their birth datetime. The result drives Thai name and number divination: the Boriwan ruler and
its lucky colour, Buddha posture, planetary strength, and the inauspicious Kalakini graha.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.thaksa import THAKSA_DECK, THAKSA_SPREAD, build_engine

request = ReadingRequest(
    deck_id=THAKSA_DECK.id,
    spread_id=THAKSA_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1990-04-15T09:00:00+07:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.thaksa
