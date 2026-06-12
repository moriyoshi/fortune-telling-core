from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Nine Star Ki tradition implementation.

The package exposes the nine-star deck, the core Nine Star Ki spread, and an
engine builder for deterministic natal and annual chart readings.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.nine_star_ki import (
        NINE_STAR_KI_DECK,
        NINE_STAR_KI_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=NINE_STAR_KI_DECK.id,
        spread_id=NINE_STAR_KI_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={
                "birth_datetime": "1990-01-01T12:00:00+00:00",
                "latitude": "51.5074",
                "longitude": "-0.1278",
            }
        ),
    )
    reading = build_engine(target_year=2026).cast(request)
    ```
"""

from fortune_telling_core.traditions.nine_star_ki.config import DayStarEscapement  # noqa: E402
from fortune_telling_core.traditions.nine_star_ki.deck import NINE_STAR_KI_DECK  # noqa: E402
from fortune_telling_core.traditions.nine_star_ki.engine import (  # noqa: E402
    NineStarKiEngine,
    build_engine,
)
from fortune_telling_core.traditions.nine_star_ki.spreads import NINE_STAR_KI_SPREAD  # noqa: E402

__all__ = [
    "DayStarEscapement",
    "NINE_STAR_KI_DECK",
    "NINE_STAR_KI_SPREAD",
    "NineStarKiEngine",
    "build_engine",
]
