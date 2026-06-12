"""Datetime serialization helpers."""

from __future__ import annotations

from datetime import UTC, datetime

from fortune_telling_core.errors import ValidationError


def utc_now() -> datetime:
    return datetime.now(UTC)


def ensure_aware(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValidationError(f"{field_name} must be timezone-aware")
    return value


def parse_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be an ISO-8601 string")
    parsed = datetime.fromisoformat(value)
    return ensure_aware(parsed, field_name)
