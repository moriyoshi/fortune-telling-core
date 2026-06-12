"""Name numerology request parsing."""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.traditions.name_numerology.config import YMode


@dataclass(frozen=True, slots=True)
class NameInput:
    name: str
    y_mode: YMode


def parse_name_input(request: ReadingRequest, default_y_mode: YMode) -> NameInput:
    values = collect_values(request)
    return NameInput(
        name=require_string(values, "name"),
        y_mode=YMode(values.get("y_mode", default_y_mode.value)),
    )
