from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Elder Futhark rune-casting tradition implementation.

The package exposes the 24-rune deck, single-rune and Norns spreads, and an
engine builder. Unlike the calendrical traditions, rune casting is RNG-driven
(like tarot): pass an ``Rng`` to ``read``. Reversals are optional via
``allow_reversals=true``, and the eight symmetrical runes are never reversed.

Example:
    ```python
    from fortune_telling_core import RandomRng, ReadingRequest
    from fortune_telling_core.traditions.runes import (
        RUNE_DECK,
        NORNS,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=RUNE_DECK.id,
        spread_id=NORNS.id,
        options={"allow_reversals": "true"},
    )
    reading = build_engine().read(request, rng=RandomRng(seed=42))
    ```
"""

from fortune_telling_core.traditions.runes.deck import RUNE_DECK  # noqa: E402
from fortune_telling_core.traditions.runes.engine import RuneEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.runes.spreads import NORNS, SINGLE_RUNE  # noqa: E402

__all__ = ["NORNS", "RUNE_DECK", "SINGLE_RUNE", "RuneEngine", "build_engine"]
