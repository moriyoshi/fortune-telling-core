# Tarot

A Rider-Waite-Smith tarot engine with a 78-card deck, single-card and three-card spreads, and
optional reversals.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.tarot import RWS_DECK, THREE_CARD, build_engine

engine = build_engine()
request = ReadingRequest(
    deck_id=RWS_DECK.id,
    spread_id=THREE_CARD.id,
    options={"allow_reversals": "true"},
)

reading = engine.read(request, rng=RandomRng(seed=20260612))
```

::: fortune_telling_core.traditions.tarot
