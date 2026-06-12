from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Four Pillars of Destiny, or BaZi, tradition implementation.

The package exposes the 22-symbol stem and branch deck, the eight-position
Four Pillars spread, and an engine builder for deterministic natal charts.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.four_pillars import (
        FOUR_PILLARS_DECK,
        FOUR_PILLARS_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=FOUR_PILLARS_DECK.id,
        spread_id=FOUR_PILLARS_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={
                "birth_datetime": "1990-01-01T12:00:00+00:00",
                "latitude": "51.5074",
                "longitude": "-0.1278",
                "gender": "male",
            }
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.four_pillars.deck import FOUR_PILLARS_DECK  # noqa: E402
from fortune_telling_core.traditions.four_pillars.engine import (  # noqa: E402
    FourPillarsEngine,
    build_engine,
)
from fortune_telling_core.traditions.four_pillars.spreads import FOUR_PILLARS_SPREAD  # noqa: E402

__all__ = ["FOUR_PILLARS_DECK", "FOUR_PILLARS_SPREAD", "FourPillarsEngine", "build_engine"]
