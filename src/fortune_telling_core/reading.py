"""Final reading value objects."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from fortune_telling_core.coerce import (
    json_object,
    json_object_sequence,
    optional_int,
    optional_str,
)
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.provenance import Provenance
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.serde_types import JsonMapping, JsonObject
from fortune_telling_core.spread import Position, Spread
from fortune_telling_core.symbols import Symbol


@dataclass(frozen=True, slots=True)
class PositionReading:
    """Resolved result for one spread position.

    Args:
        position: Spread position metadata.
        symbol: Selected symbol metadata.
        selection: Recorded selection that links the position and symbol.
    """

    position: Position
    symbol: Symbol
    selection: Selection

    def to_dict(self) -> JsonObject:
        """Serialize the position reading to a JSON-compatible dictionary."""

        return {
            "position": self.position.to_dict(),
            "symbol": self.symbol.to_dict(),
            "selection": self.selection.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: JsonMapping) -> PositionReading:
        """Deserialize a position reading.

        Args:
            data: JSON-compatible position reading mapping.

        Returns:
            The decoded position reading.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            position=Position.from_dict(json_object(data.get("position"), "position")),
            symbol=Symbol.from_dict(json_object(data.get("symbol"), "symbol")),
            selection=Selection.from_dict(json_object(data.get("selection"), "selection")),
        )


@dataclass(frozen=True, slots=True)
class Reading:
    """Complete self-contained reading.

    A reading embeds its request, spread, draw, resolved position readings, and
    provenance so it can be serialized, audited, and replayed later.

    Args:
        request: Original request.
        spread: Spread used to resolve positions.
        draw: Recorded draw.
        positions: Resolved position readings.
        summary: Optional engine-generated summary text. When present, this
            text is always plain American English.
        provenance: Audit metadata.
        schema_version: Serialized schema version.
    """

    request: ReadingRequest
    spread: Spread
    draw: Draw
    positions: Sequence[PositionReading]
    summary: str | None
    provenance: Provenance
    schema_version: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "positions", tuple(self.positions))

    def to_dict(self) -> JsonObject:
        """Serialize the reading to a JSON-compatible dictionary."""

        result: JsonObject = {
            "schema_version": self.schema_version,
            "request": self.request.to_dict(),
            "spread": self.spread.to_dict(),
            "draw": self.draw.to_dict(),
            "positions": [position.to_dict() for position in self.positions],
            "provenance": self.provenance.to_dict(),
        }
        if self.summary is not None:
            result["summary"] = self.summary
        return result

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Reading:
        """Deserialize a reading.

        Args:
            data: JSON-compatible reading mapping.

        Returns:
            The decoded reading.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            request=ReadingRequest.from_dict(json_object(data.get("request"), "request")),
            spread=Spread.from_dict(json_object(data.get("spread"), "spread")),
            draw=Draw.from_dict(json_object(data.get("draw"), "draw")),
            positions=tuple(
                PositionReading.from_dict(item)
                for item in json_object_sequence(data.get("positions"), "positions")
            ),
            summary=optional_str(data, "summary"),
            provenance=Provenance.from_dict(json_object(data.get("provenance"), "provenance")),
            schema_version=optional_int(data, "schema_version") or 1,
        )
