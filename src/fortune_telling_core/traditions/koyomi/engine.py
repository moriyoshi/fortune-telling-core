"""Koyomi (暦注) day-quality engine.

Given a civil date, the engine reports the day's 六曜, its sexagenary 干支, the
sectional solar month, and the supported 選日 flags (一粒万倍日 / 三隣亡 /
天赦日). It reuses the lunisolar converter, solar-term astronomy, and sexagenary
day count.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_from_date, julian_day_utc
from fortune_telling_core.astronomy.lunisolar import to_lunisolar
from fortune_telling_core.astronomy.solar import sun_longitude
from fortune_telling_core.astronomy.solar_terms import solar_month_index
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.four_pillars.pillars import DAY_JIAZI_JDN
from fortune_telling_core.traditions.four_pillars.sexagenary import ganzhi
from fortune_telling_core.traditions.koyomi.calendar_notes import ROKUYO, compute_day_notes
from fortune_telling_core.traditions.koyomi.deck import KOYOMI_DECK
from fortune_telling_core.traditions.koyomi.spreads import KOYOMI_SPREAD

_NULL_RNG = NullRng("KoyomiEngine.cast must not use randomness")


@dataclass(frozen=True, slots=True)
class KoyomiTarget:
    target_datetime: datetime


class KoyomiEngine(AbstractEngine):
    """Koyomi day-quality engine.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            Defaults to ``BuiltinEphemeris``.
    """

    id = "koyomi.engine"
    version = "0.1.0"

    def __init__(self, ephemeris: Ephemeris | None = None) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the koyomi rokuyō deck."""

        if request.deck_id != KOYOMI_DECK.id:
            raise ValidationError(f"unsupported koyomi deck: {request.deck_id}")
        return KOYOMI_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the koyomi day-quality spread."""

        if request.spread_id != KOYOMI_SPREAD.id:
            raise ValidationError(f"unsupported koyomi spread: {request.spread_id}")
        return KOYOMI_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the day's koyomi annotations as a deterministic draw."""

        del rng
        target = self._target(request)
        dt = target.target_datetime
        jd_tt = jd_tt_from_utc(julian_day_utc(dt))
        sekki_index = solar_month_index(sun_longitude(jd_tt, self.ephemeris))

        offset = dt.utcoffset()
        tz_hours = offset.total_seconds() / 3600.0 if offset is not None else 0.0
        lunisolar = to_lunisolar(jd_tt, tz_hours=tz_hours, ephemeris=self.ephemeris)

        day_index = (julian_day_from_date(dt.year, dt.month, dt.day) - DAY_JIAZI_JDN) % 60
        day = ganzhi(day_index)

        notes = compute_day_notes(sekki_index, lunisolar.month, lunisolar.day, day)
        slug, cjk, _ = ROKUYO[notes.rokuyo_index]
        selection = Selection(
            "rokuyo",
            f"koyomi.rokuyo.{slug}",
            {
                "rokuyo_cjk": cjk,
                "day_ganzhi": day.cjk,
                "sekki_month": str(notes.sekki_month),
                "lunisolar": (
                    f"{lunisolar.year}-"
                    f"{'leap-' if lunisolar.is_leap_month else ''}"
                    f"{lunisolar.month}-{lunisolar.day}"
                ),
                "ichiryu_manbai": str(notes.is_ichiryu_manbai).lower(),
                "sanrinbo": str(notes.is_sanrinbo).lower(),
                "tensha": str(notes.is_tensha).lower(),
            },
        )
        return Draw(KOYOMI_DECK.id, KOYOMI_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a koyomi reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = draw.selections[0].modifiers or {}
        flags = [
            name
            for name, key in (
                ("一粒万倍日", "ichiryu_manbai"),
                ("三隣亡", "sanrinbo"),
                ("天赦日", "tensha"),
            )
            if modifiers[key] == "true"
        ]
        flag_text = "、".join(flags) if flags else "none"
        summary = (
            f"Rokuyō {modifiers['rokuyo_cjk']}; day {modifiers['day_ganzhi']}; "
            f"select-days: {flag_text}."
        )
        provenance_notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            "rokuyo=(lunar_month+lunar_day)%6",
            "select_days=ichiryu_manbai,sanrinbo,tensha",
            "day_epoch=2000-01-07-jia-zi",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(
                base.provenance, notes=provenance_notes, rng_kind=None, rng_seed=None
            ),
        )

    def _target(self, request: ReadingRequest) -> KoyomiTarget:
        values = collect_values(request)
        explicit = values.get("target_datetime")
        if explicit:
            return KoyomiTarget(parse_datetime(explicit, "target_datetime"))
        if request.as_of is not None:
            return KoyomiTarget(request.as_of)
        raw = require_string(values, "birth_datetime")
        return KoyomiTarget(parse_datetime(raw, "birth_datetime"))


def build_engine(ephemeris: Ephemeris | None = None) -> KoyomiEngine:
    """Create a koyomi day-quality engine."""

    return KoyomiEngine(ephemeris=ephemeris)
