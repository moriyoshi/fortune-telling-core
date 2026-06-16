"""Four Pillars birth-data parsing."""

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
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.four_pillars.config import (
    DayBoundary,
    LuckDirectionInput,
    TimeModel,
)


@dataclass(frozen=True, slots=True)
class FourPillarsBirthData:
    birth_datetime: datetime
    latitude: float
    longitude: float
    gender: LuckDirectionInput
    time_model: TimeModel
    day_boundary: DayBoundary
    luck_count: int
    target_year: int


def parse_birth_data(request: ReadingRequest, default_luck_count: int) -> FourPillarsBirthData:
    values = collect_values(request)
    birth_datetime = parse_datetime(require_string(values, "birth_datetime"), "birth_datetime")
    latitude = parse_latitude(values)
    longitude = parse_longitude(values)
    gender = LuckDirectionInput(require_string(values, "gender"))
    luck_count = int(values.get("luck_count", str(default_luck_count)))
    if luck_count < 1:
        raise ValidationError("luck_count must be positive")
    return FourPillarsBirthData(
        birth_datetime=birth_datetime,
        latitude=latitude,
        longitude=longitude,
        gender=gender,
        time_model=TimeModel(values.get("time_model", TimeModel.CLOCK.value)),
        day_boundary=DayBoundary(values.get("day_boundary", DayBoundary.MIDNIGHT.value)),
        luck_count=luck_count,
        target_year=int(values.get("target_year") or request.effective_at.year),
    )
