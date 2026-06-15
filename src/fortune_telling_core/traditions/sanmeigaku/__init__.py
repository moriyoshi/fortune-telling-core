from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Sanmeigaku (算命学) tradition implementation.

Sanmeigaku reads the year, month, and day pillars of the sexagenary calendar
(the hour pillar is not used) and renders a body star chart (人体星図) of five
main stars (十大主星) and three subordinate stars (十二大従星). The engine reuses
the Four Pillars solar-term astronomy and Ten-God logic.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.sanmeigaku import (
        SANMEIGAKU_DECK,
        SANMEIGAKU_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=SANMEIGAKU_DECK.id,
        spread_id=SANMEIGAKU_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1984-02-02T12:00:00+09:00"},
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.sanmeigaku.config import (  # noqa: E402
    DayBoundary,
    HiddenStemRule,
    TimeModel,
)
from fortune_telling_core.traditions.sanmeigaku.deck import SANMEIGAKU_DECK  # noqa: E402
from fortune_telling_core.traditions.sanmeigaku.engine import (  # noqa: E402
    SanmeigakuEngine,
    build_engine,
)
from fortune_telling_core.traditions.sanmeigaku.spreads import SANMEIGAKU_SPREAD  # noqa: E402

__all__ = [
    "DayBoundary",
    "HiddenStemRule",
    "SANMEIGAKU_DECK",
    "SANMEIGAKU_SPREAD",
    "SanmeigakuEngine",
    "TimeModel",
    "build_engine",
]
