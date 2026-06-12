from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Domino divination tradition implementation.

The package exposes the 28-tile double-six deck, single-tile and three-tile
spreads, and an engine builder. Like tarot, casting is RNG-driven: pass an
``Rng`` to ``read``.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.dominoes import (
        DOMINOES_DECK,
        THREE_TILES,
        build_engine,
    )

    request = ReadingRequest(deck_id=DOMINOES_DECK.id, spread_id=THREE_TILES.id)
    reading = build_engine().read(request, rng=RandomRng(seed=42))
    ```
"""

from fortune_telling_core.traditions.dominoes.deck import DOMINOES_DECK  # noqa: E402
from fortune_telling_core.traditions.dominoes.engine import (  # noqa: E402
    DominoesEngine,
    build_engine,
)
from fortune_telling_core.traditions.dominoes.spreads import (  # noqa: E402
    SINGLE_TILE,
    THREE_TILES,
)

__all__ = [
    "DOMINOES_DECK",
    "SINGLE_TILE",
    "THREE_TILES",
    "DominoesEngine",
    "build_engine",
]
