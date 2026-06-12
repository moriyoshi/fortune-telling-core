from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Petit Lenormand tradition implementation.

The package exposes the 36-card deck, single-card / three-card / Grand Tableau
spreads, and an engine builder. Like tarot, casting is RNG-driven: pass an
``Rng`` to ``read``. Lenormand cards are never reversed, and the Grand Tableau
lays out the whole deck.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.lenormand import (
        LENORMAND_DECK,
        THREE_CARD,
        build_engine,
    )

    request = ReadingRequest(deck_id=LENORMAND_DECK.id, spread_id=THREE_CARD.id)
    reading = build_engine().read(request, rng=RandomRng(seed=42))
    ```
"""

from fortune_telling_core.traditions.lenormand.cards import LENORMAND_DECK  # noqa: E402
from fortune_telling_core.traditions.lenormand.engine import (  # noqa: E402
    LenormandEngine,
    build_engine,
)
from fortune_telling_core.traditions.lenormand.spreads import (  # noqa: E402
    GRAND_TABLEAU,
    SINGLE_CARD,
    THREE_CARD,
)

__all__ = [
    "GRAND_TABLEAU",
    "LENORMAND_DECK",
    "SINGLE_CARD",
    "THREE_CARD",
    "LenormandEngine",
    "build_engine",
]
