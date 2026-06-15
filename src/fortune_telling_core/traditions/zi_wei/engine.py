"""Zi Wei Dou Shu (紫微斗数) engine.

Builds the twelve-palace chart with the fourteen major stars from a birth
datetime. The engine converts the birth instant to a lunisolar date, derives
the year stem/branch, 命宮 / 身宮, the 五行局, and the 紫微 / 天府 star series,
then assigns the twelve palaces to the earthly branches.

Only the fourteen major stars are placed. Minor stars and the 四化
transformations are out of scope (they reference stars beyond the majors and
diverge between schools).
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
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.astronomy.lunisolar import to_lunisolar
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.zi_wei.chart import (
    BRANCH_CJK,
    BRANCH_SLUG,
    PALACES,
    STEM_CJK,
    ZiWeiChart,
    compute_chart,
)
from fortune_telling_core.traditions.zi_wei.deck import ZI_WEI_DECK
from fortune_telling_core.traditions.zi_wei.spreads import ZI_WEI_SPREAD

_NULL_RNG = NullRng("ZiWeiEngine.cast must not use randomness")

_BUREAU_NAME: dict[int, str] = {
    2: "水二局",
    3: "木三局",
    4: "金四局",
    5: "土五局",
    6: "火六局",
}


@dataclass(frozen=True, slots=True)
class ZiWeiBirth:
    birth_datetime: datetime


class ZiWeiEngine(AbstractEngine):
    """Zi Wei Dou Shu twelve-palace engine.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol,
            used by the lunisolar converter. Defaults to ``BuiltinEphemeris``.
    """

    id = "zi_wei.engine"
    version = "0.1.0"

    def __init__(self, ephemeris: Ephemeris | None = None) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Zi Wei branch deck."""

        if request.deck_id != ZI_WEI_DECK.id:
            raise ValidationError(f"unsupported Zi Wei deck: {request.deck_id}")
        return ZI_WEI_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Zi Wei twelve-palace spread."""

        if request.spread_id != ZI_WEI_SPREAD.id:
            raise ValidationError(f"unsupported Zi Wei spread: {request.spread_id}")
        return ZI_WEI_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Zi Wei chart as a deterministic draw."""

        del rng
        birth = self._birth(request)
        jd_tt = jd_tt_from_utc(julian_day_utc(birth.birth_datetime))
        offset = birth.birth_datetime.utcoffset()
        tz_hours = offset.total_seconds() / 3600.0 if offset is not None else 0.0
        lunisolar = to_lunisolar(jd_tt, tz_hours=tz_hours, ephemeris=self.ephemeris)
        hour_branch = ((birth.birth_datetime.hour + 1) // 2) % 12
        chart = compute_chart(
            lunisolar.year, lunisolar.month, lunisolar.day, hour_branch
        )
        return _draw_from_chart(chart)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Zi Wei reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        ming = draw.selections[0].modifiers or {}
        bureau = ming["bureau"]
        stars = ming["stars_cjk"] or "(empty)"
        summary = (
            f"Zi Wei 命宮 in {ming['branch_cjk']} ({_BUREAU_NAME.get(int(bureau), bureau)}); "
            f"命宮 stars: {stars}."
        )
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            "stars=14_major",
            "lunar_year_stem_branch=annual-index",
            "transformations=omitted",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )

    def _birth(self, request: ReadingRequest) -> ZiWeiBirth:
        values = collect_values(request)
        raw = require_string(values, "birth_datetime")
        return ZiWeiBirth(birth_datetime=parse_datetime(raw, "birth_datetime"))


def _draw_from_chart(chart: ZiWeiChart) -> Draw:
    selections: list[Selection] = []
    for index, (slug, cjk) in enumerate(PALACES):
        branch = chart.palace_branches[index]
        stars = chart.stars_by_branch[branch]
        selections.append(
            Selection(
                slug,
                f"zi_wei.branch.{BRANCH_SLUG[branch]}",
                {
                    "palace": cjk,
                    "branch_cjk": BRANCH_CJK[branch],
                    "stem_cjk": STEM_CJK[chart.palace_stems[index]],
                    "stars": ",".join(star.slug for star in stars),
                    "stars_cjk": ",".join(star.cjk for star in stars),
                    "is_body_palace": str(branch == chart.body_branch).lower(),
                    "bureau": str(chart.bureau),
                },
            )
        )
    return Draw(ZI_WEI_DECK.id, ZI_WEI_SPREAD.id, tuple(selections))


def build_engine(ephemeris: Ephemeris | None = None) -> ZiWeiEngine:
    """Create a Zi Wei Dou Shu engine."""

    return ZiWeiEngine(ephemeris=ephemeris)
