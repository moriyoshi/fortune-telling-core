from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Koyomi (暦注) day-quality tradition implementation.

Given a civil date, the engine reports the day's 六曜 (rokuyō), its sexagenary
干支, the sectional solar month, and the supported 選日 day flags (一粒万倍日,
三隣亡, 天赦日). It reuses the lunisolar converter and solar-term astronomy.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.koyomi import (
        KOYOMI_DECK,
        KOYOMI_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=KOYOMI_DECK.id,
        spread_id=KOYOMI_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"target_datetime": "2024-01-01T12:00:00+09:00"},
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.koyomi.deck import KOYOMI_DECK  # noqa: E402
from fortune_telling_core.traditions.koyomi.engine import KoyomiEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.koyomi.spreads import KOYOMI_SPREAD  # noqa: E402

__all__ = [
    "KOYOMI_DECK",
    "KOYOMI_SPREAD",
    "KoyomiEngine",
    "build_engine",
]
