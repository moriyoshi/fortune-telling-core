# Dominoes

A domino-divination engine with the 28-tile double-six deck plus single-tile and three-tile spreads.
Casting is RNG-driven: pass an `Rng` to `read`.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.dominoes import DOMINOES_DECK, THREE_TILES, build_engine

request = ReadingRequest(deck_id=DOMINOES_DECK.id, spread_id=THREE_TILES.id)
reading = build_engine().read(request, rng=RandomRng(seed=42))
```

::: fortune_telling_core.traditions.dominoes
