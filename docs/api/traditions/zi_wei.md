# Zi Wei Dou Shu (紫微斗数)

A Zi Wei Dou Shu engine that builds the twelve-palace chart with the fourteen major stars from a
birth datetime. It converts the birth instant to a lunisolar date, derives the year stem/branch,
命宮 / 身宮, the 五行局 bureau (from the 命宮 stem-branch 納音), and the 紫微 / 天府 star series, then
assigns the twelve palaces to the earthly branches.

Each palace selection's symbol is the earthly branch the palace occupies; the palace's stars, its
heavenly stem (五虎遁), and the 身宮 flag are recorded as modifiers. Only the fourteen major stars are
placed — minor stars and the 四化 transformations (which reference stars beyond the majors and diverge
between schools) are out of scope.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.zi_wei import ZI_WEI_DECK, ZI_WEI_SPREAD, build_engine

request = ReadingRequest(
    deck_id=ZI_WEI_DECK.id,
    spread_id=ZI_WEI_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={"birth_datetime": "1985-04-29T10:00:00+08:00"},
    ),
)
reading = build_engine().cast(request)
```

## Time-varying fortunes (流年 / 大限)

The summary also relocates the 命宮 pointer for a
[`as_of`](../core.md#natal-vs-timed-readings) moment (the fourteen major stars do
not move):

- **流年** (annual) — the 流年命宮 sits on the palace whose branch equals the
  target year's 太歲 branch. Always reported; the year defaults to `as_of` (or
  `requested_at`) and can be pinned with the `target_year` attribute.
- **大限** (decade limits) — each palace governs ten years; the first 大限 is the
  命宮, starting at the 五行局 number in 虚歳 (數え年, born = 1). It appears only
  when the request supplies a `gender` attribute (`male` / `female`): 陽年男・
  陰年女 → 順行 (advancing the branch), 陰年男・陽年女 → 逆行 (retreating it). The
  active decade for the target year is reported with its palace and resident
  stars.

The moving 流 stars (流昌 / 流曲 …) and the 四化 are minor/divergent and remain
out of scope, as in the natal chart.

::: fortune_telling_core.traditions.zi_wei
