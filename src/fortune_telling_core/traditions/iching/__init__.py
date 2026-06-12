from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""I Ching (Book of Changes) tradition implementation.

The package exposes the 64-hexagram deck, the casting spread, and an engine
builder. Like tarot and runes, casting is RNG-driven: pass an ``Rng`` to
``read``. The three-coin method casts six lines into a primary hexagram and,
where lines change, a relating hexagram.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.iching import (
        ICHING_DECK,
        CASTING,
        build_engine,
    )

    request = ReadingRequest(deck_id=ICHING_DECK.id, spread_id=CASTING.id)
    reading = build_engine().read(request, rng=RandomRng(seed=42))
    ```
"""

from fortune_telling_core.traditions.iching.deck import ICHING_DECK  # noqa: E402
from fortune_telling_core.traditions.iching.engine import IChingEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.iching.spreads import CASTING  # noqa: E402

__all__ = ["CASTING", "ICHING_DECK", "IChingEngine", "build_engine"]
