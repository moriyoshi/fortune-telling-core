"""Numerology birth-data parsing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core._time import parse_datetime
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.numerology.config import ReductionMethod


@dataclass(frozen=True, slots=True)
class NumerologyBirthData:
    birth_datetime: datetime
    method: ReductionMethod


def parse_birth_data(
    request: ReadingRequest,
    default_method: ReductionMethod,
) -> NumerologyBirthData:
    values = collect_values(request)
    return NumerologyBirthData(
        birth_datetime=parse_datetime(require_string(values, "birth_datetime"), "birth_datetime"),
        method=ReductionMethod(values.get("reduction_method", default_method.value)),
    )
