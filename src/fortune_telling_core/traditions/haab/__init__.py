from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Maya Haab' (365-day vague year) tradition implementation.

The package exposes the month deck (eighteen winal plus the five-day Wayeb'),
the single-position birth spread, and an engine builder that deterministically
derives a querent's Haab' date — a day position within a named month — from
their birth date. The cycle uses the GMT (584283) correlation, anchored at
21 December 2012 = 3 K'ank'in, and partners the Tzolk'in in the Calendar Round.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.haab import (
        HAAB_DECK,
        HAAB_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=HAAB_DECK.id,
        spread_id=HAAB_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "2012-12-21T00:00:00+00:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Haab' date 3 K'ank'in."
    ```
"""

from fortune_telling_core.traditions.haab.deck import HAAB_DECK  # noqa: E402
from fortune_telling_core.traditions.haab.engine import HaabEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.haab.spreads import HAAB_SPREAD  # noqa: E402

__all__ = ["HAAB_DECK", "HAAB_SPREAD", "HaabEngine", "build_engine"]
