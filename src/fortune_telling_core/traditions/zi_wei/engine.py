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

from collections.abc import Mapping
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
from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
from fortune_telling_core.traditions.zi_wei.chart import (
    BRANCH_CJK,
    BRANCH_SLUG,
    PALACES,
    STEM_CJK,
    ZiWeiChart,
    compute_chart,
)
from fortune_telling_core.traditions.zi_wei.deck import ZI_WEI_DECK
from fortune_telling_core.traditions.zi_wei.periods import active_da_xian, liunian
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
    gender: LuckDirectionInput | None
    target_year: int


class ZiWeiEngine(AbstractEngine):
    """Zi Wei Dou Shu twelve-palace engine.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol,
            used by the lunisolar converter. Defaults to ``BuiltinEphemeris``.

    Time-varying fortunes: the 流年 (annual 命宮) for ``request.as_of`` (or
    ``target_year`` / ``requested_at``) is always reported; the active 大限
    (decade limit) is added when the request supplies ``gender`` (male/female),
    which fixes its 順行 / 逆行 direction.
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
        chart = compute_chart(lunisolar.year, lunisolar.month, lunisolar.day, hour_branch)
        return _draw_from_chart(
            chart,
            target_year=birth.target_year,
            gender=birth.gender,
            birth_lunar_year=lunisolar.year,
        )

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
        ) + _periods_text(ming)
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            "stars=14_major",
            "lunar_year_stem_branch=annual-index",
            "transformations=omitted",
            f"target_year={ming['target_year']}",
            "da_xian_start_age=wuxing_bureau_in_nominal_age",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )

    def _birth(self, request: ReadingRequest) -> ZiWeiBirth:
        values = collect_values(request)
        raw = require_string(values, "birth_datetime")
        gender = LuckDirectionInput(values["gender"]) if values.get("gender") else None
        return ZiWeiBirth(
            birth_datetime=parse_datetime(raw, "birth_datetime"),
            gender=gender,
            target_year=int(values.get("target_year") or request.effective_at.year),
        )


def _draw_from_chart(
    chart: ZiWeiChart,
    *,
    target_year: int,
    gender: LuckDirectionInput | None,
    birth_lunar_year: int,
) -> Draw:
    selections: list[Selection] = []
    for index, (slug, cjk) in enumerate(PALACES):
        branch = chart.palace_branches[index]
        stars = chart.stars_by_branch[branch]
        modifiers = {
            "palace": cjk,
            "branch_cjk": BRANCH_CJK[branch],
            "stem_cjk": STEM_CJK[chart.palace_stems[index]],
            "stars": ",".join(star.slug for star in stars),
            "stars_cjk": ",".join(star.cjk for star in stars),
            "is_body_palace": str(branch == chart.body_branch).lower(),
            "bureau": str(chart.bureau),
        }
        if slug == "ming":
            modifiers.update(_period_meta(chart, target_year, gender, birth_lunar_year))
        selections.append(Selection(slug, f"zi_wei.branch.{BRANCH_SLUG[branch]}", modifiers))
    return Draw(ZI_WEI_DECK.id, ZI_WEI_SPREAD.id, tuple(selections))


def _period_meta(
    chart: ZiWeiChart,
    target_year: int,
    gender: LuckDirectionInput | None,
    birth_lunar_year: int,
) -> dict[str, str]:
    """Re-derivable pointers for the 流年 / 大限 of ``target_year``.

    Stored on the 命宮 selection so a replay reproduces them from the draw alone.
    """

    annual = liunian(chart, target_year)
    meta: dict[str, str] = {
        "target_year": str(target_year),
        "liunian_ganzhi": annual.ganzhi_cjk,
        "liunian_branch_cjk": BRANCH_CJK[annual.palace.branch],
        "liunian_palace": annual.palace.palace_cjk,
        "liunian_stars_cjk": annual.palace.stars_cjk,
    }
    if gender is not None:
        decade = active_da_xian(chart, gender, birth_lunar_year, target_year)
        meta.update(
            {
                "gender": gender.value,
                "da_xian_direction": "forward" if decade.forward else "backward",
                "da_xian_start_age": str(decade.start_age),
                "da_xian_end_age": str(decade.end_age),
                "da_xian_branch_cjk": BRANCH_CJK[decade.palace.branch],
                "da_xian_palace": decade.palace.palace_cjk,
                "da_xian_stars_cjk": decade.palace.stars_cjk,
            }
        )
    return meta


def _periods_text(ming: Mapping[str, str]) -> str:
    liunian_stars = ming["liunian_stars_cjk"] or "(empty)"
    parts = [
        f" Liunian {ming['target_year']} ({ming['liunian_ganzhi']}) 命宮 in "
        f"{ming['liunian_branch_cjk']} ({ming['liunian_palace']}): {liunian_stars}."
    ]
    if "da_xian_direction" in ming:
        da_xian_stars = ming["da_xian_stars_cjk"] or "(empty)"
        parts.append(
            f" Da Xian ({ming['da_xian_direction']}) ages "
            f"{ming['da_xian_start_age']}-{ming['da_xian_end_age']} in "
            f"{ming['da_xian_branch_cjk']} ({ming['da_xian_palace']}): {da_xian_stars}."
        )
    return "".join(parts)


def build_engine(ephemeris: Ephemeris | None = None) -> ZiWeiEngine:
    """Create a Zi Wei Dou Shu engine."""

    return ZiWeiEngine(ephemeris=ephemeris)
