from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Western geomancy tradition implementation.

The package exposes the sixteen-figure deck, the shield-chart spread, and an
engine builder. Casting is RNG-driven (like tarot): four Mother figures are
generated from random points, then the Daughters (the Mothers' transpose),
Nieces, two Witnesses, and the Judge follow by geomantic addition.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.geomancy import (
        GEOMANCY_DECK,
        SHIELD,
        build_engine,
    )

    request = ReadingRequest(deck_id=GEOMANCY_DECK.id, spread_id=SHIELD.id)
    reading = build_engine().read(request, rng=RandomRng(seed=42))
    ```
"""

from fortune_telling_core.traditions.geomancy.deck import GEOMANCY_DECK  # noqa: E402
from fortune_telling_core.traditions.geomancy.engine import (  # noqa: E402
    GeomancyEngine,
    build_engine,
)
from fortune_telling_core.traditions.geomancy.spreads import SHIELD  # noqa: E402

__all__ = ["GEOMANCY_DECK", "SHIELD", "GeomancyEngine", "build_engine"]
