"""Tradition-agnostic symbols and decks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from fortune_telling_core.coerce import (
    json_object_sequence,
    require_str,
    str_mapping,
)
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.serde_types import JsonMapping, JsonObject


@dataclass(frozen=True, slots=True)
class Symbol:
    """Tradition-neutral symbol that can appear in a deck.

    Args:
        id: Stable symbol identifier, unique inside its deck.
        name: Human-readable symbol name.
        attributes: Optional string metadata. Traditions use this for details
            such as tarot suit, zodiac element, or stem polarity.

    Raises:
        ValidationError: If `id`, `name`, or attributes are invalid.
    """

    id: str
    name: str
    attributes: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("symbol id must not be empty")
        if not self.name:
            raise ValidationError("symbol name must not be empty")
        object.__setattr__(self, "attributes", str_mapping(self.attributes, "attributes"))

    def to_dict(self) -> JsonObject:
        """Serialize the symbol to a JSON-compatible dictionary.

        Returns:
            The stable symbol representation.
        """

        return {"id": self.id, "name": self.name, "attributes": dict(self.attributes)}

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Symbol:
        """Deserialize a symbol.

        Args:
            data: JSON-compatible symbol mapping.

        Returns:
            The decoded symbol.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            id=require_str(data, "id"),
            name=require_str(data, "name"),
            attributes=str_mapping(data.get("attributes"), "attributes"),
        )


@dataclass(frozen=True, slots=True)
class Deck:
    """Ordered pool of symbols used by an engine.

    Args:
        id: Stable deck identifier.
        symbols: Ordered symbols available to the engine.
        weights: Optional positive integer weights matching `symbols`.

    Raises:
        ValidationError: If the deck is empty, has duplicate symbol ids, or has
            invalid weights.
    """

    id: str
    symbols: Sequence[Symbol]
    weights: Sequence[int] | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("deck id must not be empty")
        symbols = tuple(self.symbols)
        if not symbols:
            raise ValidationError("deck must contain at least one symbol")
        symbol_ids = [symbol.id for symbol in symbols]
        if len(set(symbol_ids)) != len(symbol_ids):
            raise ValidationError("deck symbol ids must be unique")
        object.__setattr__(self, "symbols", symbols)

        if self.weights is None:
            return
        weights = tuple(self.weights)
        if any(isinstance(weight, bool) or not isinstance(weight, int) for weight in weights):
            raise ValidationError("deck weights must be integers")
        if len(weights) != len(symbols):
            raise ValidationError("deck weights must match symbol count")
        if any(weight <= 0 for weight in weights):
            raise ValidationError("deck weights must be positive")
        object.__setattr__(self, "weights", weights)

    def symbol_by_id(self, symbol_id: str) -> Symbol | None:
        """Return a symbol by id.

        Args:
            symbol_id: Identifier to look up.

        Returns:
            The matching symbol, or `None` when absent.
        """

        for symbol in self.symbols:
            if symbol.id == symbol_id:
                return symbol
        return None

    def to_dict(self) -> JsonObject:
        """Serialize the deck to a JSON-compatible dictionary.

        Returns:
            The stable deck representation.
        """

        result: JsonObject = {
            "id": self.id,
            "symbols": [symbol.to_dict() for symbol in self.symbols],
        }
        if self.weights is not None:
            result["weights"] = list(self.weights)
        return result

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Deck:
        """Deserialize a deck.

        Args:
            data: JSON-compatible deck mapping.

        Returns:
            The decoded deck.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        weights = data.get("weights")
        parsed_weights: tuple[int, ...] | None = None
        if weights is not None:
            if not isinstance(weights, Sequence) or isinstance(weights, str):
                raise ValidationError("weights must be an array")
            parsed_weight_values: list[int] = []
            for weight in weights:
                if isinstance(weight, bool) or not isinstance(weight, int):
                    raise ValidationError("weights must contain only integer values")
                parsed_weight_values.append(weight)
            parsed_weights = tuple(parsed_weight_values)
        return cls(
            id=require_str(data, "id"),
            symbols=tuple(
                Symbol.from_dict(item)
                for item in json_object_sequence(data.get("symbols"), "symbols")
            ),
            weights=parsed_weights,
        )
