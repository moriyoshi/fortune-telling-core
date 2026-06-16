"""Sanmeigaku birth-data parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput
from fortune_telling_core.traditions.sanmeigaku.config import (
    DayBoundary,
    HiddenStemRule,
    TimeModel,
)


@dataclass(frozen=True, slots=True)
class SanmeigakuBirthData:
    """Parsed Sanmeigaku request inputs.

    ``latitude`` and ``longitude`` only affect non-clock time models; they
    default to ``0.0`` when absent. Sanmeigaku does not use the hour pillar.
    ``gender`` is optional: it is only needed for the 大運 (luck-cycle)
    direction, so the natal body star chart and 年運 work without it.
    ``target_year`` is the 年運 year, defaulting to the request's ``as_of``
    moment (``effective_at``).
    """

    birth_datetime: datetime
    latitude: float
    longitude: float
    time_model: TimeModel
    day_boundary: DayBoundary
    hidden_stem_rule: HiddenStemRule
    gender: LuckDirectionInput | None
    target_year: int


def parse_birth_data(
    request: ReadingRequest,
    *,
    time_model: TimeModel,
    day_boundary: DayBoundary,
    hidden_stem_rule: HiddenStemRule,
) -> SanmeigakuBirthData:
    values = collect_values(request)
    birth_datetime = parse_datetime(require_string(values, "birth_datetime"), "birth_datetime")
    gender = LuckDirectionInput(values["gender"]) if values.get("gender") else None
    return SanmeigakuBirthData(
        birth_datetime=birth_datetime,
        latitude=float(values.get("latitude", "0.0")),
        longitude=float(values.get("longitude", "0.0")),
        time_model=TimeModel(values["time_model"]) if "time_model" in values else time_model,
        day_boundary=(
            DayBoundary(values["day_boundary"]) if "day_boundary" in values else day_boundary
        ),
        hidden_stem_rule=(
            HiddenStemRule(values["hidden_stem_rule"])
            if "hidden_stem_rule" in values
            else hidden_stem_rule
        ),
        gender=gender,
        target_year=int(values.get("target_year") or request.effective_at.year),
    )
