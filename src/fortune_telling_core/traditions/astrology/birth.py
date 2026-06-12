"""Birth data parsing."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core._time import parse_datetime
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.astrology.config import (
    Ayanamsa,
    ChartConfig,
    HouseSystem,
    ZodiacMode,
)


@dataclass(frozen=True, slots=True)
class BirthData:
    birth_datetime: datetime
    latitude: float
    longitude: float
    config: ChartConfig


def parse_birth_data(request: ReadingRequest) -> BirthData:
    values = _merged_values(request)
    birth_datetime = parse_datetime(_require(values, "birth_datetime"), "birth_datetime")
    latitude = _require_float(values, "latitude")
    longitude = _require_float(values, "longitude")
    if latitude < -90.0 or latitude > 90.0:
        raise ValidationError("latitude must be between -90 and 90")
    if longitude < -180.0 or longitude > 180.0:
        raise ValidationError("longitude must be between -180 and 180")

    zodiac = ZodiacMode(values.get("zodiac", ZodiacMode.TROPICAL.value))
    ayanamsa_value = values.get("ayanamsa")
    ayanamsa = None if ayanamsa_value is None else Ayanamsa(ayanamsa_value)
    house_system = HouseSystem(values.get("house_system", HouseSystem.WHOLE_SIGN.value))
    high_latitude_fallback = values.get("high_latitude_fallback") == "true"
    include_angles = values.get("include_angles_in_aspects", "true") != "false"
    return BirthData(
        birth_datetime=birth_datetime,
        latitude=latitude,
        longitude=longitude,
        config=ChartConfig(
            zodiac=zodiac,
            ayanamsa=ayanamsa,
            house_system=house_system,
            high_latitude_fallback=high_latitude_fallback,
            include_angles_in_aspects=include_angles,
        ),
    )


def _merged_values(request: ReadingRequest) -> Mapping[str, str]:
    values: dict[str, str] = {}
    if request.options is not None:
        values.update(request.options)
    if request.querent is not None:
        values.update(request.querent.attributes or {})
    return values


def _require(values: Mapping[str, str], field_name: str) -> str:
    value = values.get(field_name)
    if value is None or value == "":
        raise ValidationError(f"{field_name} is required")
    return value


def _require_float(values: Mapping[str, str], field_name: str) -> float:
    raw = _require(values, field_name)
    try:
        return float(raw)
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be a float") from exc
