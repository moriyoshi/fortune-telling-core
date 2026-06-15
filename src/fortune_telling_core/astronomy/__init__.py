"""Shared astronomy primitives used by multiple traditions.

The package contains deterministic Julian-day helpers, solar-term utilities,
and an injectable ephemeris protocol. The default backend is pure Python and
has no required runtime dependencies.

Example:
    ```python
    from datetime import UTC, datetime

    from fortune_telling_core.astronomy import BuiltinEphemeris, julian_day_utc

    ephemeris = BuiltinEphemeris()
    jd_utc = julian_day_utc(datetime(2026, 6, 12, tzinfo=UTC))
    assert ephemeris.supported_bodies()
    ```
"""

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import delta_t_seconds, jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.errors import AstronomyError, EphemerisError
from fortune_telling_core.astronomy.julian import (
    julian_centuries,
    julian_day_from_date,
    julian_day_utc,
)
from fortune_telling_core.astronomy.lunisolar import (
    LunisolarDate,
    civil_day_number,
    new_moon_on_or_before,
    to_lunisolar,
)
from fortune_telling_core.astronomy.position import EclipticPosition, normalize_degrees
from fortune_telling_core.astronomy.solar import (
    equation_of_time,
    solar_longitude_crossing,
    sun_longitude,
)
from fortune_telling_core.astronomy.solar_terms import (
    JIE_LONGITUDES,
    adjacent_jie_crossing,
    lichun_crossing,
    solar_month_index,
    solar_term_crossing,
)
from fortune_telling_core.astronomy.time_model import TimeModel, effective_datetime

__all__ = [
    "AstronomyError",
    "Body",
    "BuiltinEphemeris",
    "EclipticPosition",
    "Ephemeris",
    "EphemerisError",
    "FixedEphemeris",
    "JIE_LONGITUDES",
    "LunisolarDate",
    "TimeModel",
    "adjacent_jie_crossing",
    "civil_day_number",
    "delta_t_seconds",
    "effective_datetime",
    "equation_of_time",
    "jd_tt_from_utc",
    "julian_centuries",
    "julian_day_from_date",
    "julian_day_utc",
    "lichun_crossing",
    "new_moon_on_or_before",
    "normalize_degrees",
    "solar_longitude_crossing",
    "solar_month_index",
    "solar_term_crossing",
    "sun_longitude",
    "to_lunisolar",
]
