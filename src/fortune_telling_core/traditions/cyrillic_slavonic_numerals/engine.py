"""Old Cyrillic / Church Slavonic numeral engine."""

from __future__ import annotations

from dataclasses import replace
from enum import StrEnum

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
from fortune_telling_core.traditions._name_values import cyrillic_slavonic_numerals
from fortune_telling_core.traditions._name_values.cyrillic_slavonic_numerals import (
    KoppaMode,
    LetterTable,
    Omega800Mode,
    TitloMode,
    U400Mode,
    UnvaluedLettersMode,
    XiMode,
)
from fortune_telling_core.traditions.cyrillic_slavonic_numerals.deck import (
    CYRILLIC_SLAVONIC_NUMERALS_DECK,
    CYRILLIC_SLAVONIC_NUMERALS_RESULT_SYMBOL,
)
from fortune_telling_core.traditions.cyrillic_slavonic_numerals.spreads import (
    CYRILLIC_SLAVONIC_NUMERALS_SPREAD,
)

_NULL_RNG = NullRng("CyrillicSlavonicNumeralsEngine.cast must not use randomness")


class CyrillicSlavonicNumeralsEngine(AbstractEngine):
    """Old Cyrillic / Church Slavonic numeral engine."""

    id = "cyrillic_slavonic_numerals.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Old Cyrillic numerals deck."""

        if request.deck_id != CYRILLIC_SLAVONIC_NUMERALS_DECK.id:
            raise ValidationError(f"unsupported Old Cyrillic deck: {request.deck_id}")
        return CYRILLIC_SLAVONIC_NUMERALS_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Old Cyrillic numerals spread."""

        if request.spread_id != CYRILLIC_SLAVONIC_NUMERALS_SPREAD.id:
            raise ValidationError(f"unsupported Old Cyrillic spread: {request.spread_id}")
        return CYRILLIC_SLAVONIC_NUMERALS_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Old Cyrillic total as a deterministic draw."""

        del rng
        fields = collect_values(request)
        name = require_string(fields, "name")
        letter_table = _parse(fields.get("letter_table"), LetterTable.COMMON_CHURCH_SLAVONIC)
        koppa_mode = _parse(fields.get("koppa_mode"), KoppaMode.CHERV_90)
        xi_mode = _parse(fields.get("xi_mode"), XiMode.KSI_60)
        u_400_mode = _parse(fields.get("u_400_mode"), U400Mode.UK)
        omega_800_mode = _parse(fields.get("omega_800_mode"), Omega800Mode.OMEGA)
        unvalued_letters = _parse(fields.get("unvalued_letters"), UnvaluedLettersMode.REJECT)
        titlo = _parse(fields.get("titlo"), TitloMode.OPTIONAL)

        units = cyrillic_slavonic_numerals.values(
            name,
            letter_table=letter_table,
            koppa_mode=koppa_mode,
            xi_mode=xi_mode,
            u_400_mode=u_400_mode,
            omega_800_mode=omega_800_mode,
            unvalued_letters=unvalued_letters,
            titlo=titlo,
        )
        if not units:
            raise ValidationError("name must contain at least one Old Cyrillic numeral letter")
        total = cyrillic_slavonic_numerals.total(units)

        selection = Selection(
            "total",
            CYRILLIC_SLAVONIC_NUMERALS_RESULT_SYMBOL,
            {
                "value": str(total),
                "total": str(total),
                "value_system": cyrillic_slavonic_numerals.ID,
                "value_system_version": cyrillic_slavonic_numerals.VERSION,
                "letter_table": letter_table.value,
                "koppa_mode": koppa_mode.value,
                "xi_mode": xi_mode.value,
                "u_400_mode": u_400_mode.value,
                "omega_800_mode": omega_800_mode.value,
                "unvalued_letters": unvalued_letters.value,
                "titlo": titlo.value,
                "normalized_name": "".join(unit.char for unit in units),
                "values": format_value_trace(units),
            },
        )
        return Draw(
            CYRILLIC_SLAVONIC_NUMERALS_DECK.id,
            CYRILLIC_SLAVONIC_NUMERALS_SPREAD.id,
            (selection,),
        )

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute an Old Cyrillic numerals reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = f"Old Cyrillic numeral total {modifiers['total']}."
        notes = tuple(base.provenance.notes) + (
            "system=cyrillic_slavonic_numerals",
            f"value_system={cyrillic_slavonic_numerals.ID}",
            f"letter_table={modifiers['letter_table']}",
            f"koppa_mode={modifiers['koppa_mode']}",
            f"xi_mode={modifiers['xi_mode']}",
            f"u_400_mode={modifiers['u_400_mode']}",
            f"omega_800_mode={modifiers['omega_800_mode']}",
            f"unvalued_letters={modifiers['unvalued_letters']}",
            f"titlo={modifiers['titlo']}",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _parse[T: StrEnum](value: str | None, default: T) -> T:
    if value is None or value == "":
        return default
    try:
        return type(default)(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported {type(default).__name__}: {value!r}") from exc


def build_engine() -> CyrillicSlavonicNumeralsEngine:
    """Create an Old Cyrillic / Church Slavonic numeral engine."""

    return CyrillicSlavonicNumeralsEngine()
