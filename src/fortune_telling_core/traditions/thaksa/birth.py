"""Thaksa birth-data parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.request import ReadingRequest


@dataclass(frozen=True, slots=True)
class ThaksaBirthData:
    birth_datetime: datetime


def parse_birth_data(request: ReadingRequest) -> ThaksaBirthData:
    values = collect_values(request)
    return ThaksaBirthData(
        birth_datetime=parse_datetime(require_string(values, "birth_datetime"), "birth_datetime"),
    )
