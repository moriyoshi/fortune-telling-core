# Koyomi (暦注)

A koyomi day-quality engine. Given a civil date, it reports the day's 六曜 (rokuyō), its
sexagenary 干支, the sectional solar month, and the supported 選日 day flags: 一粒万倍日, 三隣亡,
and 天赦日. It reuses the lunisolar converter, solar-term astronomy, and the sexagenary day count.

The annotations that lacked a single authoritative public definition (不成就日, whose day pattern
differs between sources, and the calendrical 二十八宿 cycle, which had no verifiable epoch anchor) are
intentionally omitted rather than guessed.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.koyomi import KOYOMI_DECK, KOYOMI_SPREAD, build_engine

request = ReadingRequest(
    deck_id=KOYOMI_DECK.id,
    spread_id=KOYOMI_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"target_datetime": "2024-01-01T12:00:00+09:00"},
    ),
)
reading = build_engine().cast(request)
```

The day to evaluate may also be supplied as the request-level
[`as_of`](../core.md#natal-vs-timed-readings) moment instead of the `target_datetime` attribute;
an explicit `target_datetime` takes precedence when both are given.

::: fortune_telling_core.traditions.koyomi
