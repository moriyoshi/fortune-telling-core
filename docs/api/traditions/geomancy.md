# Western Geomancy

A geomancy engine with the sixteen-figure deck and the shield-chart spread. Casting is RNG-driven:
four Mother figures are generated from random points, then the Daughters, Nieces, two Witnesses, and
the Judge follow by geomantic addition.

```python
from fortune_telling_core import RandomRng, ReadingRequest
from fortune_telling_core.traditions.geomancy import GEOMANCY_DECK, SHIELD, build_engine

request = ReadingRequest(deck_id=GEOMANCY_DECK.id, spread_id=SHIELD.id)
reading = build_engine().read(request, rng=RandomRng(seed=42))
```

::: fortune_telling_core.traditions.geomancy
