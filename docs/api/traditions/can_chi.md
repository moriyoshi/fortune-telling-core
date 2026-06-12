# Can Chi

A Vietnamese Can Chi (Thiên Can – Địa Chi) engine that deterministically computes the sexagenary day
and hour pillars from a birth datetime — pure calendar arithmetic, no ephemeris. Each branch carries
its con giáp zodiac animal (with the Vietnamese Cat and Water Buffalo). The day pillar shares Four
Pillars' anchor; the year pillar (tuổi) is omitted because it rolls over at Tết.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.can_chi import CAN_CHI_DECK, CAN_CHI_SPREAD, build_engine

request = ReadingRequest(
    deck_id=CAN_CHI_DECK.id,
    spread_id=CAN_CHI_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1984-02-02T12:00:00+07:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.can_chi
