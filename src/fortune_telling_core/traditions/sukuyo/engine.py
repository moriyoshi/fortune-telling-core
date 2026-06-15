"""Sukuyō (宿曜) birth-mansion engine.

The engine derives the birth mansion (本命宿) from the Moon's sidereal ecliptic
longitude at birth, using the bundled ephemeris. The mansion is the equal
13°20′ division of the 27-mansion (二十七宿) sidereal zodiac that the Moon
occupies; the sidereal zero-point is selected via the ``ayanamsa`` option.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.sukuyo.config import Ayanamsa, Method
from fortune_telling_core.traditions.sukuyo.deck import SUKUYO_DECK
from fortune_telling_core.traditions.sukuyo.mansions import (
    ayanamsa_degrees,
    mansion_for_longitude,
)
from fortune_telling_core.traditions.sukuyo.spreads import SUKUYO_SPREAD

_NULL_RNG = NullRng("SukuyoEngine.cast must not use randomness")


@dataclass(frozen=True, slots=True)
class SukuyoBirthData:
    birth_datetime: datetime
    ayanamsa: Ayanamsa
    method: Method


class SukuyoEngine(AbstractEngine):
    """Sukuyō birth-mansion engine.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            Defaults to ``BuiltinEphemeris``.
        ayanamsa: Default sidereal zero-point used when the request does not
            specify one.
        method: Default birth-mansion method used when the request does not
            specify one.
    """

    id = "sukuyo.engine"
    version = "0.1.0"

    def __init__(
        self,
        ephemeris: Ephemeris | None = None,
        *,
        ayanamsa: Ayanamsa = Ayanamsa.LAHIRI,
        method: Method = Method.MOON_LONGITUDE,
    ) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()
        self.ayanamsa = ayanamsa
        self.method = method

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Sukuyō 27-mansion deck."""

        if request.deck_id != SUKUYO_DECK.id:
            raise ValidationError(f"unsupported Sukuyō deck: {request.deck_id}")
        return SUKUYO_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Sukuyō birth-mansion spread."""

        if request.spread_id != SUKUYO_SPREAD.id:
            raise ValidationError(f"unsupported Sukuyō spread: {request.spread_id}")
        return SUKUYO_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the birth mansion as a deterministic draw."""

        del rng
        birth = self._birth(request)
        jd_tt = jd_tt_from_utc(julian_day_utc(birth.birth_datetime))
        moon_longitude = self.ephemeris.position(Body.MOON, jd_tt).longitude
        mansion = mansion_for_longitude(moon_longitude, jd_tt, birth.ayanamsa)
        sidereal = (moon_longitude - ayanamsa_degrees(jd_tt, birth.ayanamsa)) % 360.0
        selection = Selection(
            "birth_mansion",
            f"sukuyo.mansion.{mansion.slug}",
            {
                "cjk": mansion.cjk,
                "nakshatra": mansion.nakshatra,
                "mansion_index": str(mansion.index),
                "moon_longitude": f"{moon_longitude:.6f}",
                "sidereal_longitude": f"{sidereal:.6f}",
                "ayanamsa": birth.ayanamsa.value,
            },
        )
        return Draw(SUKUYO_DECK.id, SUKUYO_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Sukuyō reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        birth = self._birth(request)
        modifiers = draw.selections[0].modifiers or {}
        summary = (
            f"Sukuyō birth mansion {modifiers['cjk']} ({modifiers['nakshatra']}); "
            f"sidereal Moon longitude {modifiers['sidereal_longitude']}°."
        )
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            f"method={birth.method.value}",
            f"ayanamsa={birth.ayanamsa.value}",
            "mansion_count=27",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )

    def _birth(self, request: ReadingRequest) -> SukuyoBirthData:
        values = collect_values(request)
        birth_datetime = parse_datetime(require_string(values, "birth_datetime"), "birth_datetime")
        ayanamsa = Ayanamsa(values["ayanamsa"]) if "ayanamsa" in values else self.ayanamsa
        method = Method(values["method"]) if "method" in values else self.method
        return SukuyoBirthData(birth_datetime=birth_datetime, ayanamsa=ayanamsa, method=method)


def build_engine(
    ephemeris: Ephemeris | None = None,
    *,
    ayanamsa: Ayanamsa = Ayanamsa.LAHIRI,
    method: Method = Method.MOON_LONGITUDE,
) -> SukuyoEngine:
    """Create a Sukuyō engine."""

    return SukuyoEngine(ephemeris=ephemeris, ayanamsa=ayanamsa, method=method)
