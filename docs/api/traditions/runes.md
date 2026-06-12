# Elder Futhark Runes

An Elder Futhark rune-casting engine with the 24-rune deck plus single-rune and Norns spreads.
Casting is RNG-driven. Reversals are optional via `allow_reversals`, and the eight symmetrical runes
are never reversed.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.runes import RUNE_DECK, NORNS, build_engine

request = ReadingRequest(
    deck_id=RUNE_DECK.id,
    spread_id=NORNS.id,
    options={"allow_reversals": "true"},
)
reading = build_engine().read(request, rng=RandomRng(seed=42))
```

::: fortune_telling_core.traditions.runes
