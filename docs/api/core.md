# Core API

The tradition-agnostic core: value types, the engine contract, randomness, serialisation, and
errors. These symbols are re-exported from the top-level `fortune_telling_core` package.

## Natal vs. timed readings

A reading has two distinct moments. `birth_datetime` (a per-tradition querent attribute) fixes the
*natal* chart and never changes. `ReadingRequest.as_of` is the moment you want time-varying fortunes
computed **for** — the luck/annual pillars (大運/流年), flying-star charts, almanac days, and similar
period results are derived from it. When `as_of` is unset, `ReadingRequest.effective_at` falls back
to `requested_at`, so existing callers are unaffected.

```python
from datetime import UTC, datetime

# Same person, two different points in time — only `as_of` changes.
request = ReadingRequest(
    deck_id=deck_id,
    spread_id=spread_id,
    querent=querent,  # carries birth_datetime, location, etc.
    as_of=datetime(2030, 1, 1, tzinfo=UTC),
)
```

`as_of` is the unified successor to the older per-tradition `target_year` / `target_datetime`
options. Those options still work and take precedence over `as_of` when supplied, so they remain
available for callers that only need to override a single year or date.

::: fortune_telling_core
