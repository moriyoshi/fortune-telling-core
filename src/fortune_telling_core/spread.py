"""Tradition-agnostic spread positions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from fortune_telling_core.coerce import json_object_sequence, require_str
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.serde_types import JsonMapping, JsonObject


@dataclass(frozen=True, slots=True)
class Position:
    """One named slot in a spread.

    Args:
        id: Stable position identifier.
        name: Human-readable position name.
        description: Optional explanation of the position's role.

    Raises:
        ValidationError: If `id` or `name` is empty.
    """

    id: str
    name: str
    description: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("position id must not be empty")
        if not self.name:
            raise ValidationError("position name must not be empty")

    def to_dict(self) -> JsonObject:
        """Serialize the position to a JSON-compatible dictionary."""

        return {"id": self.id, "name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Position:
        """Deserialize a position.

        Args:
            data: JSON-compatible position mapping.

        Returns:
            The decoded position.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            id=require_str(data, "id"),
            name=require_str(data, "name"),
            description=str(data.get("description", "")),
        )


@dataclass(frozen=True, slots=True)
class Spread:
    """Ordered set of positions filled by a draw.

    Args:
        id: Stable spread identifier.
        name: Human-readable spread name.
        positions: Ordered positions in the spread.

    Raises:
        ValidationError: If the spread is empty or contains duplicate position
            ids.
    """

    id: str
    name: str
    positions: Sequence[Position]

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("spread id must not be empty")
        if not self.name:
            raise ValidationError("spread name must not be empty")
        positions = tuple(self.positions)
        if not positions:
            raise ValidationError("spread must contain at least one position")
        position_ids = [position.id for position in positions]
        if len(set(position_ids)) != len(position_ids):
            raise ValidationError("spread position ids must be unique")
        object.__setattr__(self, "positions", positions)

    @property
    def size(self) -> int:
        """Number of positions in the spread."""

        return len(self.positions)

    def to_dict(self) -> JsonObject:
        """Serialize the spread to a JSON-compatible dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "positions": [position.to_dict() for position in self.positions],
        }

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Spread:
        """Deserialize a spread.

        Args:
            data: JSON-compatible spread mapping.

        Returns:
            The decoded spread.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            id=require_str(data, "id"),
            name=require_str(data, "name"),
            positions=tuple(
                Position.from_dict(item)
                for item in json_object_sequence(data.get("positions"), "positions")
            ),
        )
