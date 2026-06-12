"""Internal JSON-ish typing helpers."""

from __future__ import annotations

from collections.abc import Mapping

type JsonValue = None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type JsonMapping = Mapping[str, JsonValue]
