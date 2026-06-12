from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Vietnamese Can Chi (Thiên Can - Địa Chi) tradition implementation.

The package exposes the stem/branch deck, the day-and-hour pillar spread, and an
engine builder that deterministically computes the sexagenary day and hour
pillars from a birth datetime — pure calendar arithmetic, no ephemeris. Each
branch carries its con giáp zodiac animal (with the Vietnamese Cat and Water
Buffalo). The day pillar shares Four Pillars' anchor, so the two agree on every
calendar day. The year pillar (tuổi) is omitted because it rolls over at Tết,
which requires a lunar calendar.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.can_chi import (
        CAN_CHI_DECK,
        CAN_CHI_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=CAN_CHI_DECK.id,
        spread_id=CAN_CHI_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1984-02-02T12:00:00+07:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Day pillar Giáp Tý (Rat). Hour pillar Canh Ngọ (Horse)."
    ```
"""

from fortune_telling_core.traditions.can_chi.config import DayBoundary  # noqa: E402
from fortune_telling_core.traditions.can_chi.deck import CAN_CHI_DECK  # noqa: E402
from fortune_telling_core.traditions.can_chi.engine import (  # noqa: E402
    CanChiEngine,
    build_engine,
)
from fortune_telling_core.traditions.can_chi.spreads import CAN_CHI_SPREAD  # noqa: E402

__all__ = [
    "CAN_CHI_DECK",
    "CAN_CHI_SPREAD",
    "DayBoundary",
    "CanChiEngine",
    "build_engine",
]
