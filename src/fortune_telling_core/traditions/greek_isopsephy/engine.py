"""Greek isopsephy engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions._name_text import format_value_trace
from fortune_telling_core.traditions._name_values import greek_isopsephy
from fortune_telling_core.traditions._name_values.greek_isopsephy import (
    DiacriticsMode,
    Era,
    SigmaMode,
)
from fortune_telling_core.traditions.greek_isopsephy.deck import (
    GREEK_ISOPSEPHY_DECK,
    GREEK_ISOPSEPHY_RESULT_SYMBOL,
)
from fortune_telling_core.traditions.greek_isopsephy.spreads import GREEK_ISOPSEPHY_SPREAD

_NULL_RNG = NullRng("GreekIsopsephyEngine.cast must not use randomness")


class GreekIsopsephyEngine(AbstractEngine):
    """Greek isopsephy engine."""

    id = "greek_isopsephy.engine"
    version = "0.1.0"

    def __init__(
        self,
        *,
        era: Era = Era.CLASSICAL,
        diacritics: DiacriticsMode = DiacriticsMode.STRIPPED,
        sigma_mode: SigmaMode = SigmaMode.FINAL_TO_SIGMA,
    ) -> None:
        self.era = era
        self.diacritics = diacritics
        self.sigma_mode = sigma_mode

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Greek isopsephy deck."""

        if request.deck_id != GREEK_ISOPSEPHY_DECK.id:
            raise ValidationError(f"unsupported Greek isopsephy deck: {request.deck_id}")
        return GREEK_ISOPSEPHY_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Greek isopsephy spread."""

        if request.spread_id != GREEK_ISOPSEPHY_SPREAD.id:
            raise ValidationError(f"unsupported Greek isopsephy spread: {request.spread_id}")
        return GREEK_ISOPSEPHY_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the isopsephy total as a deterministic draw."""

        del rng
        fields = collect_values(request)
        name = require_string(fields, "name")
        era = _parse_era(fields.get("era"), self.era)
        diacritics = _parse_diacritics(fields.get("diacritics"), self.diacritics)
        sigma_mode = _parse_sigma_mode(fields.get("sigma_mode"), self.sigma_mode)

        units = greek_isopsephy.values(
            name,
            era=era,
            diacritics=diacritics,
            sigma_mode=sigma_mode,
        )
        if not units:
            raise ValidationError("name must contain at least one Greek letter")
        total = greek_isopsephy.total(units)

        selection = Selection(
            "total",
            GREEK_ISOPSEPHY_RESULT_SYMBOL,
            {
                "value": str(total),
                "total": str(total),
                "value_system": greek_isopsephy.ID,
                "value_system_version": greek_isopsephy.VERSION,
                "era": era.value,
                "diacritics": diacritics.value,
                "sigma_mode": sigma_mode.value,
                "normalized_name": "".join(unit.char for unit in units),
                "values": format_value_trace(units),
            },
        )
        return Draw(GREEK_ISOPSEPHY_DECK.id, GREEK_ISOPSEPHY_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Greek isopsephy reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = f"Isopsephy total {modifiers['total']}."
        notes = tuple(base.provenance.notes) + (
            "system=greek_isopsephy",
            f"value_system={greek_isopsephy.ID}",
            f"era={modifiers['era']}",
            f"diacritics={modifiers['diacritics']}",
            f"sigma_mode={modifiers['sigma_mode']}",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _parse_era(value: str | None, default: Era) -> Era:
    if value is None or value == "":
        return default
    try:
        return Era(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported era: {value!r}") from exc


def _parse_diacritics(value: str | None, default: DiacriticsMode) -> DiacriticsMode:
    if value is None or value == "":
        return default
    try:
        return DiacriticsMode(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported diacritics: {value!r}") from exc


def _parse_sigma_mode(value: str | None, default: SigmaMode) -> SigmaMode:
    if value is None or value == "":
        return default
    try:
        return SigmaMode(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported sigma_mode: {value!r}") from exc


def build_engine(
    *,
    era: Era = Era.CLASSICAL,
    diacritics: DiacriticsMode = DiacriticsMode.STRIPPED,
    sigma_mode: SigmaMode = SigmaMode.FINAL_TO_SIGMA,
) -> GreekIsopsephyEngine:
    """Create a Greek isopsephy engine."""

    return GreekIsopsephyEngine(era=era, diacritics=diacritics, sigma_mode=sigma_mode)
