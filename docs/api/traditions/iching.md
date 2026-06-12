# I Ching

A Book of Changes engine with the 64-hexagram deck and the three-coin casting spread. Casting is
RNG-driven: six lines form a primary hexagram and, where lines change, a relating hexagram.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.iching import ICHING_DECK, CASTING, build_engine

request = ReadingRequest(deck_id=ICHING_DECK.id, spread_id=CASTING.id)
reading = build_engine().read(request, rng=RandomRng(seed=42))
```

::: fortune_telling_core.traditions.iching
