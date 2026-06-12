"""Schema-versioned JSON helpers."""

from __future__ import annotations

import json

from fortune_telling_core.coerce import json_object
from fortune_telling_core.errors import SchemaVersionError, ValidationError
from fortune_telling_core.reading import Reading

SCHEMA_VERSION = 1


def reading_to_json(reading: Reading) -> str:
    """Serialize a reading to compact, deterministic JSON.

    Args:
        reading: Reading to encode.

    Returns:
        A JSON string with sorted keys and no insignificant whitespace.
    """

    return json.dumps(reading.to_dict(), sort_keys=True, separators=(",", ":"))


def reading_from_json(value: str) -> Reading:
    """Deserialize a reading from JSON.

    Args:
        value: JSON string produced by `reading_to_json` or the same schema.

    Returns:
        The decoded reading.

    Raises:
        SchemaVersionError: If the payload declares a future schema version.
        ValidationError: If `schema_version` or required fields are malformed.
        json.JSONDecodeError: If `value` is not valid JSON.
    """

    parsed = json.loads(value)
    data = json_object(parsed, "reading")
    version = data.get("schema_version", SCHEMA_VERSION)
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValidationError("schema_version must be an integer")
    if version > SCHEMA_VERSION:
        raise SchemaVersionError(f"unsupported schema version: {version}")
    return Reading.from_dict(data)
