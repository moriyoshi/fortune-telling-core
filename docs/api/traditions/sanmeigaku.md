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

## Time-varying fortunes (年運 / 大運)

Beyond the natal chart, the summary reports the period stars for a
[`as_of`](../core.md#natal-vs-timed-readings) moment:

- **年運** (annual stars) — the calendar year's 干支 mapped to a 主星 / 従星 for
  the day master. Always rendered; the year defaults to `as_of` (or
  `requested_at`) and can be pinned with the `target_year` attribute.
- **大運** (luck cycles) — ten-year columns advancing (順行) or retreating (逆行)
  from the month pillar. These are direction-dependent, so they appear only when
  the request supplies a `gender` attribute (`male` / `female`): 陽年男・陰年女
  → 順行, 陰年男・陽年女 → 逆行. Each column carries its 干支 and 主星 / 従星; the
  start age uses the same 節入りまでの日数 ÷ 3 convention as the Four Pillars
  engine (schools differ on the exact 起運 rule). `build_engine(luck_count=...)`
  sets how many columns are rendered.

::: fortune_telling_core.traditions.sanmeigaku
