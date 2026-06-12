"""Reading provenance and audit metadata."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime

from fortune_telling_core._time import ensure_aware, parse_datetime, utc_now
from fortune_telling_core.coerce import optional_str, require_str, str_sequence
from fortune_telling_core.serde_types import JsonMapping, JsonObject


@dataclass(frozen=True, slots=True)
class Provenance:
    """Audit metadata attached to a reading.

    Args:
        engine_id: Engine identifier.
        engine_version: Engine version string.
        library_version: `fortune-telling-core` version string.
        deck_id: Deck used by the reading.
        spread_id: Spread used by the reading.
        rng_kind: Optional RNG kind for random traditions.
        rng_seed: Optional RNG seed serialized as text.
        created_at: Timezone-aware creation timestamp.
        notes: Additional key-value style audit notes.

    Raises:
        ValidationError: If `created_at` is not timezone-aware.
    """

    engine_id: str
    engine_version: str
    library_version: str
    deck_id: str
    spread_id: str
    rng_kind: str | None = None
    rng_seed: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    notes: Sequence[str] = ()

    def __post_init__(self) -> None:
        ensure_aware(self.created_at, "created_at")
        object.__setattr__(self, "notes", tuple(self.notes))

    def to_dict(self) -> JsonObject:
        """Serialize provenance to a JSON-compatible dictionary."""

        result: JsonObject = {
            "engine_id": self.engine_id,
            "engine_version": self.engine_version,
            "library_version": self.library_version,
            "deck_id": self.deck_id,
            "spread_id": self.spread_id,
            "created_at": self.created_at.isoformat(),
            "notes": list(self.notes),
        }
        if self.rng_kind is not None:
            result["rng_kind"] = self.rng_kind
        if self.rng_seed is not None:
            result["rng_seed"] = self.rng_seed
        return result

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Provenance:
        """Deserialize provenance.

        Args:
            data: JSON-compatible provenance mapping.

        Returns:
            The decoded provenance.

        Raises:
            ValidationError: If required fields are missing or malformed.
        """

        created_at = data.get("created_at")
        return cls(
            engine_id=require_str(data, "engine_id"),
            engine_version=require_str(data, "engine_version"),
            library_version=require_str(data, "library_version"),
            deck_id=require_str(data, "deck_id"),
            spread_id=require_str(data, "spread_id"),
            rng_kind=optional_str(data, "rng_kind"),
            rng_seed=optional_str(data, "rng_seed"),
            created_at=utc_now()
            if created_at is None
            else parse_datetime(created_at, "created_at"),
            notes=str_sequence(data.get("notes", []), "notes"),
        )
