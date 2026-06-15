from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Zi Wei Dou Shu (紫微斗数) tradition implementation.

Builds the twelve-palace chart with the fourteen major stars from a birth
datetime: lunisolar conversion, year stem/branch, 命宮 / 身宮, the 五行局
bureau, and the 紫微 / 天府 star series. Minor stars and the 四化
transformations are out of scope.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.zi_wei import (
        ZI_WEI_DECK,
        ZI_WEI_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=ZI_WEI_DECK.id,
        spread_id=ZI_WEI_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1985-04-29T10:00:00+08:00"},
        ),
    )
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.traditions.zi_wei.deck import ZI_WEI_DECK  # noqa: E402
from fortune_telling_core.traditions.zi_wei.engine import ZiWeiEngine, build_engine  # noqa: E402
from fortune_telling_core.traditions.zi_wei.spreads import ZI_WEI_SPREAD  # noqa: E402

__all__ = [
    "ZI_WEI_DECK",
    "ZI_WEI_SPREAD",
    "ZiWeiEngine",
    "build_engine",
]
