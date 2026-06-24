from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Natal astrology tradition implementation.

The package exposes tropical and sidereal zodiac decks, the natal spread, the
lightweight sun-sign spread (which needs only the querent's zodiac sign), the
injectable ephemeris protocol and bundled ephemeris implementations, and an
engine builder.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.astrology import (
        NATAL_CHART,
        TROPICAL_ZODIAC,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=TROPICAL_ZODIAC.id,
        spread_id=NATAL_CHART.id,
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
    reading = build_engine().cast(request)
    ```
"""

from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris  # noqa: E402
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris  # noqa: E402
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris  # noqa: E402
from fortune_telling_core.traditions.astrology.dates import (  # noqa: E402
    sign_for_date,
    zodiac_date_range,
)
from fortune_telling_core.traditions.astrology.engine import (  # noqa: E402
    AstrologyEngine,
    build_engine,
)
from fortune_telling_core.traditions.astrology.spreads import (  # noqa: E402
    NATAL_CHART,
    SUN_SIGN,
)
from fortune_telling_core.traditions.astrology.zodiac import (  # noqa: E402
    SIDEREAL_ZODIAC,
    TROPICAL_ZODIAC,
    Sign,
)

__all__ = [
    "NATAL_CHART",
    "SIDEREAL_ZODIAC",
    "SUN_SIGN",
    "TROPICAL_ZODIAC",
    "AstrologyEngine",
    "BuiltinEphemeris",
    "Ephemeris",
    "FixedEphemeris",
    "Sign",
    "build_engine",
    "sign_for_date",
    "zodiac_date_range",
]
