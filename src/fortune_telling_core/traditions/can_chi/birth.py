"""Can Chi birth-data parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.can_chi.config import DayBoundary


@dataclass(frozen=True, slots=True)
class CanChiBirthData:
    birth_datetime: datetime
    day_boundary: DayBoundary


def parse_birth_data(
    request: ReadingRequest,
    default_day_boundary: DayBoundary,
) -> CanChiBirthData:
    values = collect_values(request)
    return CanChiBirthData(
        birth_datetime=parse_datetime(require_string(values, "birth_datetime"), "birth_datetime"),
        day_boundary=DayBoundary(values.get("day_boundary", default_day_boundary.value)),
    )
