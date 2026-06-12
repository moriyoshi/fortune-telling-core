from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Rider-Waite-Smith tarot reference implementation.

The package exposes a ready-to-use deck, supported spreads, and a small engine
builder for random tarot readings.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.tarot import RWS_DECK, SINGLE_CARD, build_engine

    request = ReadingRequest(
        deck_id=RWS_DECK.id,
        spread_id=SINGLE_CARD.id,
    )
    reading = build_engine().read(request, RandomRng(seed=7))
    ```
"""

from fortune_telling_core.traditions.tarot.cards import RWS_DECK  # noqa: E402
from fortune_telling_core.traditions.tarot.engine import TarotEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.tarot.spreads import SINGLE_CARD, THREE_CARD  # noqa: E402

__all__ = ["RWS_DECK", "SINGLE_CARD", "THREE_CARD", "TarotEngine", "build_engine"]
