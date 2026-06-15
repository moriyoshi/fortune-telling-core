"""Sanmeigaku (算命学) engine.

Sanmeigaku derives a body star chart (人体星図) from the year, month, and day
pillars of the sexagenary calendar. It reuses the Four Pillars solar-term
astronomy and Ten-God logic, then renames the results into the Sanmeigaku star
families (十大主星 / 十二大従星).
"""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.draw import Draw
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.four_pillars.config import DayBoundary, LuckDirectionInput
from fortune_telling_core.traditions.four_pillars.pillars import compute_pillars
from fortune_telling_core.traditions.four_pillars.time_model import effective_datetime
from fortune_telling_core.traditions.sanmeigaku.birth import SanmeigakuBirthData, parse_birth_data
from fortune_telling_core.traditions.sanmeigaku.chart import draw_from_pillars
from fortune_telling_core.traditions.sanmeigaku.config import HiddenStemRule, TimeModel
from fortune_telling_core.traditions.sanmeigaku.deck import SANMEIGAKU_DECK
from fortune_telling_core.traditions.sanmeigaku.spreads import SANMEIGAKU_SPREAD

_NULL_RNG = NullRng("SanmeigakuEngine.cast must not use randomness")

# Sanmeigaku does not use luck cycles; the day pillar is gender-independent.
_LUCK_GENDER = LuckDirectionInput.MALE


class SanmeigakuEngine(AbstractEngine):
    """Sanmeigaku body star chart engine.

    Args:
        ephemeris: Optional backend implementing the shared ephemeris protocol.
            Defaults to ``BuiltinEphemeris``.
        time_model: Default time-adjustment model used when the request does
            not specify one.
        day_boundary: Default day-boundary rule used when the request does not
            specify one.
        hidden_stem_rule: Default principal hidden-stem (元命) selection rule.
    """

    id = "sanmeigaku.engine"
    version = "0.1.0"

    def __init__(
        self,
        ephemeris: Ephemeris | None = None,
        *,
        time_model: TimeModel = TimeModel.CLOCK,
        day_boundary: DayBoundary = DayBoundary.MIDNIGHT,
        hidden_stem_rule: HiddenStemRule = HiddenStemRule.PRIMARY,
    ) -> None:
        self.ephemeris = ephemeris or BuiltinEphemeris()
        self.time_model = time_model
        self.day_boundary = day_boundary
        self.hidden_stem_rule = hidden_stem_rule

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Sanmeigaku star deck."""

        if request.deck_id != SANMEIGAKU_DECK.id:
            raise ValidationError(f"unsupported Sanmeigaku deck: {request.deck_id}")
        return SANMEIGAKU_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Sanmeigaku body star chart spread."""

        if request.spread_id != SANMEIGAKU_SPREAD.id:
            raise ValidationError(f"unsupported Sanmeigaku spread: {request.spread_id}")
        return SANMEIGAKU_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Sanmeigaku chart as a deterministic draw."""

        del rng
        birth = self._birth(request)
        effective = effective_datetime(
            birth.birth_datetime, birth.longitude, birth.time_model, self.ephemeris
        )
        pillars = compute_pillars(
            birth.birth_datetime,
            effective,
            self.ephemeris,
            _LUCK_GENDER,
            birth.day_boundary,
        )
        return draw_from_pillars(pillars)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Sanmeigaku reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        birth = self._birth(request)
        summary = _summary_from_draw(draw)
        notes = tuple(base.provenance.notes) + (
            f"ephemeris={self.ephemeris.id}@{self.ephemeris.version}",
            f"time_model={birth.time_model.value}",
            f"day_boundary={birth.day_boundary.value}",
            f"hidden_stem_rule={birth.hidden_stem_rule.value}",
            "pillars=year-month-day",
            "day_epoch=1984-02-02-jia-zi",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )

    def _birth(self, request: ReadingRequest) -> SanmeigakuBirthData:
        return parse_birth_data(
            request,
            time_model=self.time_model,
            day_boundary=self.day_boundary,
            hidden_stem_rule=self.hidden_stem_rule,
        )


def _summary_from_draw(draw: Draw) -> str:
    by_position = {selection.position_id: selection for selection in draw.selections}

    def cjk(position: str) -> str:
        modifiers = by_position[position].modifiers or {}
        return modifiers.get("star_cjk", "")

    center = cjk("day_branch")
    mains = "・".join(
        cjk(position)
        for position in ("year_stem", "month_stem", "year_branch", "month_branch", "day_branch")
    )
    subordinates = "・".join(
        cjk(position)
        for position in (
            "year_branch_subordinate",
            "month_branch_subordinate",
            "day_branch_subordinate",
        )
    )
    return (
        f"Sanmeigaku centre star {center}. "
        f"Main stars: {mains}. Subordinate stars: {subordinates}."
    )


def build_engine(
    ephemeris: Ephemeris | None = None,
    *,
    time_model: TimeModel = TimeModel.CLOCK,
    day_boundary: DayBoundary = DayBoundary.MIDNIGHT,
    hidden_stem_rule: HiddenStemRule = HiddenStemRule.PRIMARY,
) -> SanmeigakuEngine:
    """Create a Sanmeigaku engine."""

    return SanmeigakuEngine(
        ephemeris=ephemeris,
        time_model=time_model,
        day_boundary=day_boundary,
        hidden_stem_rule=hidden_stem_rule,
    )
