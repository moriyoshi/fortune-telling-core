from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Thai Thaksa (ทักษา) tradition implementation.

The package exposes the eight-graha deck, the eight-house Thaksa spread, and an
engine builder that deterministically seats the grahas into a querent's houses
from their birth datetime. The result drives Thai name and number divination:
the Boriwan ruler and its lucky color, Buddha posture, and planetary strength,
plus the inauspicious Kalakini graha.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.thaksa import (
        THAKSA_DECK,
        THAKSA_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=THAKSA_DECK.id,
        spread_id=THAKSA_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1990-04-15T09:00:00+07:00"},
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.thaksa.deck import THAKSA_DECK  # noqa: E402
from fortune_telling_core.traditions.thaksa.engine import ThaksaEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.thaksa.spreads import THAKSA_SPREAD  # noqa: E402

__all__ = ["THAKSA_DECK", "THAKSA_SPREAD", "ThaksaEngine", "build_engine"]
