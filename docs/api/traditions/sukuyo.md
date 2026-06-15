# Sukuyō (宿曜)

A Sukuyō astrology engine that derives a birth mansion (本命宿) from the Moon's sidereal ecliptic
longitude at birth, using the bundled ephemeris. The 27 mansions (二十七宿) are equal 13°20′ sidereal
divisions coinciding with the nakshatras; the sidereal zero-point is selected via the `Ayanamsa`
option (default Lahiri). The traditional lunisolar-table method is not bundled.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.sukuyo import SUKUYO_DECK, SUKUYO_SPREAD, build_engine

request = ReadingRequest(
    deck_id=SUKUYO_DECK.id,
    spread_id=SUKUYO_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1990-05-17T09:30:00+09:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.sukuyo
