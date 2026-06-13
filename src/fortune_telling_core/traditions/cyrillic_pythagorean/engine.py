"""Modern Cyrillic Pythagorean numerology engine."""

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
from fortune_telling_core.traditions._name_values import cyrillic_pythagorean
from fortune_telling_core.traditions._name_values.cyrillic_pythagorean import (
    Alphabet,
    Language,
    NormalizationMode,
    ShortIMode,
    SignsMode,
    YoMode,
)
from fortune_telling_core.traditions.cyrillic_pythagorean.deck import (
    CYRILLIC_PYTHAGOREAN_DECK,
)
from fortune_telling_core.traditions.cyrillic_pythagorean.spreads import (
    CYRILLIC_PYTHAGOREAN_SPREAD,
)

_NULL_RNG = NullRng("CyrillicPythagoreanEngine.cast must not use randomness")


class CyrillicPythagoreanEngine(AbstractEngine):
    """Modern Cyrillic Pythagorean numerology engine."""

    id = "cyrillic_pythagorean.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Cyrillic Pythagorean deck."""

        if request.deck_id != CYRILLIC_PYTHAGOREAN_DECK.id:
            raise ValidationError(f"unsupported Cyrillic Pythagorean deck: {request.deck_id}")
        return CYRILLIC_PYTHAGOREAN_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Cyrillic Pythagorean spread."""

        if request.spread_id != CYRILLIC_PYTHAGOREAN_SPREAD.id:
            raise ValidationError(f"unsupported Cyrillic Pythagorean spread: {request.spread_id}")
        return CYRILLIC_PYTHAGOREAN_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Cyrillic Pythagorean name number as a deterministic draw."""

        del rng
        fields = collect_values(request)
        name = require_string(fields, "name")
        language = _parse(fields.get("language"), Language.RUSSIAN)
        alphabet = _parse_optional_alphabet(fields.get("alphabet"))
        yo_mode = _parse(fields.get("yo_mode"), YoMode.DISTINCT)
        signs_mode = _parse(fields.get("signs_mode"), SignsMode.COUNT)
        short_i_mode = _parse(fields.get("short_i_mode"), ShortIMode.DISTINCT)
        normalization = _parse(fields.get("normalization"), NormalizationMode.STRICT_CYRILLIC)

        units = cyrillic_pythagorean.values(
            name,
            language=language,
            alphabet=alphabet,
            yo_mode=yo_mode,
            signs_mode=signs_mode,
            short_i_mode=short_i_mode,
            normalization=normalization,
        )
        if not units:
            raise ValidationError("name must contain at least one Cyrillic letter")
        total = cyrillic_pythagorean.total(units)
        root = cyrillic_pythagorean.reduce_to_root(total)
        resolved_alphabet = alphabet or cyrillic_pythagorean._DEFAULT_ALPHABET[language]

        selection = Selection(
            "name_number",
            f"cyrillic_pythagorean.number.{root}",
            {
                "value": str(root),
                "total": str(total),
                "value_system": cyrillic_pythagorean.ID,
                "value_system_version": cyrillic_pythagorean.VERSION,
                "language": language.value,
                "alphabet": resolved_alphabet.value,
                "yo_mode": yo_mode.value,
                "signs_mode": signs_mode.value,
                "short_i_mode": short_i_mode.value,
                "normalization": normalization.value,
                "normalized_name": "".join(unit.char for unit in units),
                "values": format_value_trace(units),
            },
        )
        return Draw(CYRILLIC_PYTHAGOREAN_DECK.id, CYRILLIC_PYTHAGOREAN_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Cyrillic Pythagorean reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = f"Cyrillic Pythagorean root {modifiers['value']} from total {modifiers['total']}."
        notes = tuple(base.provenance.notes) + (
            "system=cyrillic_pythagorean",
            f"value_system={cyrillic_pythagorean.ID}",
            f"language={modifiers['language']}",
            f"alphabet={modifiers['alphabet']}",
            f"yo_mode={modifiers['yo_mode']}",
            f"signs_mode={modifiers['signs_mode']}",
            f"short_i_mode={modifiers['short_i_mode']}",
            f"normalization={modifiers['normalization']}",
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


def _parse_optional_alphabet(value: str | None) -> Alphabet | None:
    if value is None or value == "":
        return None
    try:
        return Alphabet(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported alphabet: {value!r}") from exc


def build_engine() -> CyrillicPythagoreanEngine:
    """Create a Cyrillic Pythagorean numerology engine."""

    return CyrillicPythagoreanEngine()
