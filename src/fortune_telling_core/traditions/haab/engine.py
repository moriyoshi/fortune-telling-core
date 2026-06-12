"""Haab' engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core.draw import Draw
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.haab.birth import parse_birth_data
from fortune_telling_core.traditions.haab.chart import draw_from_date
from fortune_telling_core.traditions.haab.deck import HAAB_DECK
from fortune_telling_core.traditions.haab.months import haab_for
from fortune_telling_core.traditions.haab.spreads import HAAB_SPREAD

_NULL_RNG = NullRng("HaabEngine.cast must not use randomness")


class HaabEngine(AbstractEngine):
    """Maya Haab' (365-day vague year) engine.

    The engine deterministically derives a querent's Haab' date — a day position
    within one of eighteen winal or the five-day Wayeb' — from their birth date,
    using the GMT (584283) correlation anchored at 21 December 2012 = 3 K'ank'in.
    """

    id = "haab.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Haab' month deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``HAAB_DECK.id``.

        Returns:
            The bundled Haab' deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != HAAB_DECK.id:
            raise ValidationError(f"unsupported Haab' deck: {request.deck_id}")
        return HAAB_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Haab' spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``HAAB_SPREAD.id``.

        Returns:
            The bundled Haab' spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != HAAB_SPREAD.id:
            raise ValidationError(f"unsupported Haab' spread: {request.spread_id}")
        return HAAB_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Haab' date as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` in options or
                querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the single Haab' selection.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        del rng
        birth = parse_birth_data(request)
        return draw_from_date(haab_for(birth.birth_datetime.date()))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Haab' reading without a caller RNG.

        Args:
            request: Reading request containing birth data.

        Returns:
            A reading with the Haab' placement and summary.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        wayeb = " — Wayeb' (unlucky days)" if modifiers["wayeb"] == "true" else ""
        summary = f"Haab' date {modifiers['haab']}{wayeb}."
        notes = tuple(base.provenance.notes) + (
            "correlation=gmt-584283",
            "anchor=2012-12-21-3-kankin",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine() -> HaabEngine:
    """Create a Haab' engine.

    Returns:
        A new ``HaabEngine`` instance.
    """

    return HaabEngine()
