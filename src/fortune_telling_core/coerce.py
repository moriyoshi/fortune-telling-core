"""Internal coercion helpers for hand-written serializers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.serde_types import JsonMapping, JsonObject, JsonValue


def require_str(data: JsonMapping, field_name: str) -> str:
    value = data.get(field_name)
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    return value


def optional_str(data: JsonMapping, field_name: str) -> str | None:
    value = data.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string when provided")
    return value


def optional_int(data: JsonMapping, field_name: str) -> int | None:
    value = data.get(field_name)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field_name} must be an integer when provided")
    return value


def str_mapping(value: object, field_name: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValidationError(f"{field_name} must be an object")
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValidationError(f"{field_name} must contain only string keys and values")
        result[key] = item
    return result


def json_object(value: object, field_name: str) -> JsonObject:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{field_name} must be an object")
    return cast(JsonObject, dict(value))


def json_object_sequence(value: object, field_name: str) -> tuple[JsonObject, ...]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ValidationError(f"{field_name} must be an array")
    return tuple(json_object(item, field_name) for item in value)


def str_sequence(value: object, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ValidationError(f"{field_name} must be an array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValidationError(f"{field_name} must contain only strings")
        result.append(item)
    return tuple(result)


def json_value_mapping(value: object, field_name: str) -> dict[str, JsonValue]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValidationError(f"{field_name} must be an object")
    result: dict[str, JsonValue] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ValidationError(f"{field_name} must contain only string keys")
        result[key] = cast(JsonValue, item)
    return result
