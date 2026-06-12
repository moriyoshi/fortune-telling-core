"""Nine Star Ki birth-data parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._parsing import (
    collect_values,
    parse_latitude,
    parse_longitude,
    require_string,
)
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.astronomy.time_model import TimeModel
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.nine_star_ki.config import DayStarEscapement


@dataclass(frozen=True, slots=True)
class NineStarKiBirthData:
    birth_datetime: datetime
    latitude: float
    longitude: float
    time_model: TimeModel
    day_star_escapement: DayStarEscapement
    target_year: int


def parse_birth_data(
    request: ReadingRequest,
    default_target_year: int | None,
    default_day_star_escapement: DayStarEscapement,
) -> NineStarKiBirthData:
    values = collect_values(request)
    return NineStarKiBirthData(
        birth_datetime=parse_datetime(require_string(values, "birth_datetime"), "birth_datetime"),
        latitude=parse_latitude(values),
        longitude=parse_longitude(values),
        time_model=TimeModel(values.get("time_model", TimeModel.CLOCK.value)),
        day_star_escapement=DayStarEscapement(
            values.get("day_star_escapement", default_day_star_escapement.value)
        ),
        target_year=int(
            values.get("target_year", str(default_target_year or request.requested_at.year))
        ),
    )
