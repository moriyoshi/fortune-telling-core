"""Replayable draw artefacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from fortune_telling_core.coerce import json_object_sequence, require_str, str_mapping
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.serde_types import JsonMapping, JsonObject


@dataclass(frozen=True, slots=True)
class Selection:
    """A single chosen symbol for one spread position.

    `Selection` is the smallest replay unit in the core model. Engines may
    attach tradition-specific state in `modifiers`, but the core treats every
    modifier as an opaque string.

    Args:
        position_id: Identifier of the spread position this selection fills.
        symbol_id: Identifier of the selected symbol in the active deck.
        modifiers: Optional per-selection string metadata, such as tarot
            orientation or computed astrology longitude.

    Raises:
        ValidationError: If `position_id`, `symbol_id`, or modifier keys/values
            are invalid.
    """

    position_id: str
    symbol_id: str
    modifiers: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.position_id:
            raise ValidationError("selection position_id must not be empty")
        if not self.symbol_id:
            raise ValidationError("selection symbol_id must not be empty")
        object.__setattr__(self, "modifiers", str_mapping(self.modifiers, "modifiers"))

    def to_dict(self) -> JsonObject:
        """Serialize the selection to the stable JSON-compatible schema.

        Returns:
            A dictionary containing `position_id`, `symbol_id`, and
            `modifiers`.
        """

        return {
            "position_id": self.position_id,
            "symbol_id": self.symbol_id,
            "modifiers": dict(self.modifiers or {}),
        }

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Selection:
        """Deserialize a selection from the stable schema.

        Args:
            data: JSON-compatible mapping produced by `to_dict`.

        Returns:
            The decoded selection.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            position_id=require_str(data, "position_id"),
            symbol_id=require_str(data, "symbol_id"),
            modifiers=str_mapping(data.get("modifiers"), "modifiers"),
        )


@dataclass(frozen=True, slots=True)
class Draw:
    """Recorded, replayable outcome of selecting symbols for a spread.

    A `Draw` is authoritative for replay. Engines can interpret a recorded draw
    without consulting an RNG or, for computed traditions, an ephemeris.

    Args:
        deck_id: Identifier of the deck used for all selections.
        spread_id: Identifier of the spread whose positions were filled.
        selections: Ordered selections, one per spread position.
        extras: Optional structured selections that are *not* bound to a spread
            position — variable-count, computed facts an engine wants to expose
            for interpretation (e.g. astrology aspects). Unlike ``selections``
            they carry no per-position uniqueness or spread-binding contract;
            they default to empty and are serialized only when present.

    Raises:
        ValidationError: If identifiers are empty, there are no selections, or
            a position appears more than once.
    """

    deck_id: str
    spread_id: str
    selections: Sequence[Selection]
    extras: Sequence[Selection] = ()

    def __post_init__(self) -> None:
        if not self.deck_id:
            raise ValidationError("draw deck_id must not be empty")
        if not self.spread_id:
            raise ValidationError("draw spread_id must not be empty")
        selections = tuple(self.selections)
        if not selections:
            raise ValidationError("draw must contain at least one selection")
        position_ids = [selection.position_id for selection in selections]
        if len(set(position_ids)) != len(position_ids):
            raise ValidationError("draw must contain one selection per position")
        object.__setattr__(self, "selections", selections)
        object.__setattr__(self, "extras", tuple(self.extras))

    def to_dict(self) -> JsonObject:
        """Serialize the draw to the stable JSON-compatible schema.

        Returns:
            A dictionary containing deck, spread, and selection data, plus
            ``extras`` when any are present.
        """

        result: JsonObject = {
            "deck_id": self.deck_id,
            "spread_id": self.spread_id,
            "selections": [selection.to_dict() for selection in self.selections],
        }
        if self.extras:
            result["extras"] = [extra.to_dict() for extra in self.extras]
        return result

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Draw:
        """Deserialize a draw from the stable schema.

        Args:
            data: JSON-compatible mapping produced by `to_dict`.

        Returns:
            The decoded draw.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            deck_id=require_str(data, "deck_id"),
            spread_id=require_str(data, "spread_id"),
            selections=tuple(
                Selection.from_dict(item)
                for item in json_object_sequence(data.get("selections"), "selections")
            ),
            extras=tuple(
                Selection.from_dict(item)
                for item in json_object_sequence(data.get("extras") or [], "extras")
            ),
        )
