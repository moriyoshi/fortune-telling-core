from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Maya Tzolk'in (260-day sacred round) tradition implementation.

The package exposes the twenty-day-sign deck, the single-position birth spread,
and an engine builder that deterministically derives a querent's Tzolk'in day —
a trecena number (1-13) paired with a day sign — from their birth date. The
cycle uses the GMT (584283) correlation, anchored at 21 December 2012 = 4 Ajaw.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.tzolkin import (
        TZOLKIN_DECK,
        TZOLKIN_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=TZOLKIN_DECK.id,
        spread_id=TZOLKIN_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "2012-12-21T00:00:00+00:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Tzolk'in day 4 Ajaw (Lord, south)."
    ```
"""

from fortune_telling_core.traditions.tzolkin.deck import TZOLKIN_DECK  # noqa: E402
from fortune_telling_core.traditions.tzolkin.engine import (  # noqa: E402
    TzolkinEngine,
    build_engine,
)
from fortune_telling_core.traditions.tzolkin.spreads import TZOLKIN_SPREAD  # noqa: E402

__all__ = ["TZOLKIN_DECK", "TZOLKIN_SPREAD", "TzolkinEngine", "build_engine"]
