from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Chaldean numerology tradition implementation.

The package exposes the nine planetary root numbers, the name-number spread, and
an engine builder that deterministically reduces a name to its Chaldean root
(1-9) using the Chaldean letter values (1-8, with nine never assigned to a
letter). This is distinct from the Pythagorean name numerology tradition.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.chaldean_numerology import (
        CHALDEAN_NUMEROLOGY_DECK,
        CHALDEAN_NUMEROLOGY_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=CHALDEAN_NUMEROLOGY_DECK.id,
        spread_id=CHALDEAN_NUMEROLOGY_SPREAD.id,
        querent=Querent(id="s", display_name="Sample", attributes={"name": "John"}),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Name number 9 (Mars); total 18."
    ```
"""

from fortune_telling_core.traditions.chaldean_numerology.deck import (  # noqa: E402
    CHALDEAN_NUMEROLOGY_DECK,
)
from fortune_telling_core.traditions.chaldean_numerology.engine import (  # noqa: E402
    ChaldeanNumerologyEngine,
    build_engine,
)
from fortune_telling_core.traditions.chaldean_numerology.spreads import (  # noqa: E402
    CHALDEAN_NUMEROLOGY_SPREAD,
)

__all__ = [
    "CHALDEAN_NUMEROLOGY_DECK",
    "CHALDEAN_NUMEROLOGY_SPREAD",
    "ChaldeanNumerologyEngine",
    "build_engine",
]
