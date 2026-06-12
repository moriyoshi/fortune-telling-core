# Petit Lenormand

A Petit Lenormand engine with the 36-card deck and single-card, three-card, and Grand Tableau
spreads. Casting is RNG-driven; Lenormand cards are never reversed, and the Grand Tableau lays out
the whole deck.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.lenormand import LENORMAND_DECK, THREE_CARD, build_engine

request = ReadingRequest(deck_id=LENORMAND_DECK.id, spread_id=THREE_CARD.id)
reading = build_engine().read(request, rng=RandomRng(seed=42))
```

::: fortune_telling_core.traditions.lenormand
