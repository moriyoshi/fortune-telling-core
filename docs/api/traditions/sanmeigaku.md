# Sanmeigaku (算命学)

A Sanmeigaku engine that derives a body star chart (人体星図) from the year, month, and day pillars
of the sexagenary calendar (the hour pillar is not used). It reuses the Four Pillars solar-term
astronomy and Ten-God logic, renaming the results into the Sanmeigaku star families: five main stars
(十大主星) and three subordinate stars (十二大従星).

Star positions are recorded by their source stem or branch. The geographic 人体星図 arrangement
(北/南/東/西/中央 and the shoulder/foot cells) and the 初年/中年/晩年 life-stage labelling vary
between teachers and are left to an interpretation layer. The principal hidden stem (元命) defaults to
each branch's primary qi (本気); see `HiddenStemRule`.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.sanmeigaku import (
    SANMEIGAKU_DECK,
    SANMEIGAKU_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=SANMEIGAKU_DECK.id,
    spread_id=SANMEIGAKU_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1984-02-02T12:00:00+09:00"},
    ),
)
reading = build_engine().cast(request)
```

::: fortune_telling_core.traditions.sanmeigaku
