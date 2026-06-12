from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Javanese weton (Primbon) tradition implementation.

The package exposes the weton deck (seven saptawara days and five pancawara
pasaran), the birth weton spread, and an engine builder that deterministically
derives a querent's weton and neptu from their birth datetime.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.weton import (
        WETON_DECK,
        WETON_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=WETON_DECK.id,
        spread_id=WETON_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1945-08-17T10:00:00+07:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Weton Jumat Legi: neptu 6 + 5 = 11."
    ```
"""

from fortune_telling_core.traditions.weton.config import DayBoundary  # noqa: E402
from fortune_telling_core.traditions.weton.deck import WETON_DECK  # noqa: E402
from fortune_telling_core.traditions.weton.engine import WetonEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.weton.spreads import WETON_SPREAD  # noqa: E402

__all__ = [
    "DayBoundary",
    "WETON_DECK",
    "WETON_SPREAD",
    "WetonEngine",
    "build_engine",
]
