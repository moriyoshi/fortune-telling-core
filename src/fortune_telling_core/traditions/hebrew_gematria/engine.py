"""Hebrew gematria engine."""

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
from fortune_telling_core.traditions._name_values import hebrew_gematria
from fortune_telling_core.traditions._name_values.hebrew_gematria import FinalLetterMode
from fortune_telling_core.traditions.hebrew_gematria.deck import (
    HEBREW_GEMATRIA_DECK,
    HEBREW_GEMATRIA_RESULT_SYMBOL,
)
from fortune_telling_core.traditions.hebrew_gematria.spreads import HEBREW_GEMATRIA_SPREAD

_NULL_RNG = NullRng("HebrewGematriaEngine.cast must not use randomness")


class HebrewGematriaEngine(AbstractEngine):
    """Hebrew gematria engine.

    The engine deterministically sums the standard gematria values of a Hebrew
    name. Gematria compares raw totals rather than reducing to a single digit,
    so the total is the symbol-bearing value and is stamped into the selection
    modifiers over a single structural result symbol.

    Args:
        final_letter_mode: Default treatment of final forms (sofit) when the
            request does not specify ``final_letter_mode``.
    """

    id = "hebrew_gematria.engine"
    version = "0.1.0"

    def __init__(self, *, final_letter_mode: FinalLetterMode = FinalLetterMode.STANDARD) -> None:
        self.final_letter_mode = final_letter_mode

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Hebrew gematria deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``HEBREW_GEMATRIA_DECK.id``.

        Returns:
            The bundled deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != HEBREW_GEMATRIA_DECK.id:
            raise ValidationError(f"unsupported Hebrew gematria deck: {request.deck_id}")
        return HEBREW_GEMATRIA_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Hebrew gematria spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``HEBREW_GEMATRIA_SPREAD.id``.

        Returns:
            The bundled spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != HEBREW_GEMATRIA_SPREAD.id:
            raise ValidationError(f"unsupported Hebrew gematria spread: {request.spread_id}")
        return HEBREW_GEMATRIA_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the gematria total as a deterministic draw.

        Args:
            request: Reading request with ``name`` and optional
                ``final_letter_mode`` in options or querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the single total selection.

        Raises:
            ValidationError: If the name is missing, has no Hebrew letters, or
                ``final_letter_mode`` is invalid.
        """

        del rng
        fields = collect_values(request)
        name = require_string(fields, "name")
        mode = _parse_final_letter_mode(fields.get("final_letter_mode"), self.final_letter_mode)

        units = hebrew_gematria.values(name, final_letter_mode=mode)
        if not units:
            raise ValidationError("name must contain at least one Hebrew letter")
        total = hebrew_gematria.total(units)

        selection = Selection(
            "total",
            HEBREW_GEMATRIA_RESULT_SYMBOL,
            {
                "value": str(total),
                "total": str(total),
                "value_system": hebrew_gematria.ID,
                "value_system_version": hebrew_gematria.VERSION,
                "final_letter_mode": mode.value,
                "normalized_name": "".join(unit.char for unit in units),
                "values": format_value_trace(units),
            },
        )
        return Draw(HEBREW_GEMATRIA_DECK.id, HEBREW_GEMATRIA_SPREAD.id, (selection,))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Hebrew gematria reading without a caller RNG.

        Args:
            request: Reading request containing the name and optional
                configuration.

        Returns:
            A reading with the total placement and structural summary.

        Raises:
            ValidationError: If the name or options are invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = f"Gematria total {modifiers['total']}."
        notes = tuple(base.provenance.notes) + (
            "system=hebrew_gematria",
            f"value_system={hebrew_gematria.ID}",
            "vowels=ignored",
            f"final_letters={modifiers['final_letter_mode']}",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _parse_final_letter_mode(value: str | None, default: FinalLetterMode) -> FinalLetterMode:
    if value is None or value == "":
        return default
    try:
        return FinalLetterMode(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported final_letter_mode: {value!r}") from exc


def build_engine(
    *, final_letter_mode: FinalLetterMode = FinalLetterMode.STANDARD
) -> HebrewGematriaEngine:
    """Create a Hebrew gematria engine.

    Args:
        final_letter_mode: Default treatment of final forms (sofit).

    Returns:
        A new ``HebrewGematriaEngine`` instance.
    """

    return HebrewGematriaEngine(final_letter_mode=final_letter_mode)
