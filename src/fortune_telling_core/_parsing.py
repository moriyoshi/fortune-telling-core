"""Shared request parsing helpers."""

from __future__ import annotations

from collections.abc import Mapping

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.request import ReadingRequest


def collect_values(request: ReadingRequest) -> dict[str, str]:
    values: dict[str, str] = {}
    if request.options is not None:
        values.update(request.options)
    if request.querent is not None:
        values.update(request.querent.attributes or {})
    return values


def require_string(values: Mapping[str, str], field_name: str) -> str:
    value = values.get(field_name)
    if value is None or value == "":
        raise ValidationError(f"{field_name} is required")
    return value


def parse_float(values: Mapping[str, str], field_name: str) -> float:
    try:
        return float(require_string(values, field_name))
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be a float") from exc


def parse_latitude(values: Mapping[str, str], field_name: str = "latitude") -> float:
    latitude = parse_float(values, field_name)
    if latitude < -90.0 or latitude > 90.0:
        raise ValidationError("latitude must be between -90 and 90")
    return latitude


def parse_longitude(values: Mapping[str, str], field_name: str = "longitude") -> float:
    longitude = parse_float(values, field_name)
    if longitude < -180.0 or longitude > 180.0:
        raise ValidationError("longitude must be between -180 and 180")
    return longitude
