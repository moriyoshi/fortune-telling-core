from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Sukuyō (宿曜) tradition implementation.

Sukuyō astrology assigns a birth mansion (本命宿) from the Moon's position at
birth. This engine uses the sidereal Moon-longitude method over the 27 lunar
mansions (二十七宿) and exposes the ayanamsa (sidereal zero-point) as a
configurable option.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.sukuyo import (
        SUKUYO_DECK,
        SUKUYO_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=SUKUYO_DECK.id,
        spread_id=SUKUYO_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1990-05-17T09:30:00+09:00"},
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.sukuyo.config import Ayanamsa, Method  # noqa: E402
from fortune_telling_core.traditions.sukuyo.deck import SUKUYO_DECK  # noqa: E402
from fortune_telling_core.traditions.sukuyo.engine import SukuyoEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.sukuyo.spreads import SUKUYO_SPREAD  # noqa: E402

__all__ = [
    "Ayanamsa",
    "Method",
    "SUKUYO_DECK",
    "SUKUYO_SPREAD",
    "SukuyoEngine",
    "build_engine",
]
