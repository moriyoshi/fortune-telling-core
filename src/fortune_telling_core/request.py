"""Reading request value objects."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime

from fortune_telling_core._time import ensure_aware, parse_datetime, utc_now
from fortune_telling_core.coerce import json_object, require_str, str_mapping
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.serde_types import JsonMapping, JsonObject


@dataclass(frozen=True, slots=True)
class Querent:
    """Person or subject for whom a reading is made.

    Args:
        id: Stable application-level identifier.
        display_name: Human-readable name for display.
        attributes: Optional string metadata. Computed traditions use these
            fields for birth data when supplied.

    Raises:
        ValidationError: If identifiers or attributes are invalid.
    """

    id: str
    display_name: str
    attributes: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("querent id must not be empty")
        if not self.display_name:
            raise ValidationError("querent display_name must not be empty")
        object.__setattr__(self, "attributes", str_mapping(self.attributes, "attributes"))

    def to_dict(self) -> JsonObject:
        """Serialize the querent to a JSON-compatible dictionary."""

        return {
            "id": self.id,
            "display_name": self.display_name,
            "attributes": dict(self.attributes or {}),
        }

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Querent:
        """Deserialize a querent.

        Args:
            data: JSON-compatible querent mapping.

        Returns:
            The decoded querent.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        return cls(
            id=require_str(data, "id"),
            display_name=require_str(data, "display_name"),
            attributes=str_mapping(data.get("attributes"), "attributes"),
        )


@dataclass(frozen=True, slots=True)
class ReadingRequest:
    """Input used by an engine to produce or replay a reading.

    Args:
        spread_id: Identifier of the requested spread.
        deck_id: Identifier of the requested deck.
        querent: Optional querent metadata.
        options: Engine-specific string options.
        requested_at: Timezone-aware request timestamp.
        as_of: Optional timezone-aware moment the reading should be computed
            *for*. Traditions that report time-varying fortunes (luck/annual
            pillars, flying-star charts, almanac days, transits) read this as
            the reference point, falling back to ``requested_at`` when unset.
            This is the unified successor to the per-tradition ``target_year`` /
            ``target_datetime`` options, which still override it.

    Raises:
        ValidationError: If identifiers, options, or timestamps are invalid.
    """

    spread_id: str
    deck_id: str
    querent: Querent | None = None
    options: Mapping[str, str] | None = None
    requested_at: datetime = field(default_factory=utc_now)
    as_of: datetime | None = None

    def __post_init__(self) -> None:
        if not self.spread_id:
            raise ValidationError("request spread_id must not be empty")
        if not self.deck_id:
            raise ValidationError("request deck_id must not be empty")
        ensure_aware(self.requested_at, "requested_at")
        if self.as_of is not None:
            ensure_aware(self.as_of, "as_of")
        object.__setattr__(self, "options", str_mapping(self.options, "options"))

    @property
    def effective_at(self) -> datetime:
        """Reference moment for time-varying fortunes.

        Returns ``as_of`` when set, otherwise ``requested_at``. This is the
        single source of truth a tradition should consult when it needs the
        "as of" moment but has no explicit per-tradition override.
        """

        return self.as_of if self.as_of is not None else self.requested_at

    def to_dict(self) -> JsonObject:
        """Serialize the request to a JSON-compatible dictionary."""

        result: JsonObject = {
            "spread_id": self.spread_id,
            "deck_id": self.deck_id,
            "options": dict(self.options or {}),
            "requested_at": self.requested_at.isoformat(),
        }
        if self.as_of is not None:
            result["as_of"] = self.as_of.isoformat()
        if self.querent is not None:
            result["querent"] = self.querent.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: JsonMapping) -> ReadingRequest:
        """Deserialize a reading request.

        Args:
            data: JSON-compatible request mapping.

        Returns:
            The decoded request.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        querent_data = data.get("querent")
        querent = (
            None
            if querent_data is None
            else Querent.from_dict(json_object(querent_data, "querent"))
        )
        requested_at = data.get("requested_at")
        as_of = data.get("as_of")
        return cls(
            spread_id=require_str(data, "spread_id"),
            deck_id=require_str(data, "deck_id"),
            querent=querent,
            options=str_mapping(data.get("options"), "options"),
            requested_at=utc_now()
            if requested_at is None
            else parse_datetime(requested_at, "requested_at"),
            as_of=None if as_of is None else parse_datetime(as_of, "as_of"),
        )
