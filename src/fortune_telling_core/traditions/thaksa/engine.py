"""Thaksa engine."""

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
from fortune_telling_core.traditions.thaksa.birth import parse_birth_data
from fortune_telling_core.traditions.thaksa.chart import compute_chart, draw_from_chart
from fortune_telling_core.traditions.thaksa.deck import THAKSA_DECK
from fortune_telling_core.traditions.thaksa.spreads import THAKSA_SPREAD

_NULL_RNG = NullRng("ThaksaEngine.cast must not use randomness")


class ThaksaEngine(AbstractEngine):
    """Thai Thaksa (ทักษา) engine.

    The engine deterministically derives a querent's birth-day ruling graha and
    seats the eight grahas into the eight Thaksa houses, surfacing the ruler's
    lucky color, Buddha posture, planetary strength, and the inauspicious
    Kalakini graha. A Wednesday birth at or after 18:00 rules under Rahu
    (Wednesday night).
    """

    id = "thaksa.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Thaksa graha deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``THAKSA_DECK.id``.

        Returns:
            The bundled Thaksa deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != THAKSA_DECK.id:
            raise ValidationError(f"unsupported Thaksa deck: {request.deck_id}")
        return THAKSA_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Thaksa house spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``THAKSA_SPREAD.id``.

        Returns:
            The bundled Thaksa spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != THAKSA_SPREAD.id:
            raise ValidationError(f"unsupported Thaksa spread: {request.spread_id}")
        return THAKSA_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the Thaksa house placements as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` in options or
                querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with one graha selection per Thaksa house.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        del rng
        birth = parse_birth_data(request)
        return draw_from_chart(compute_chart(birth.birth_datetime))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Thaksa reading without a caller RNG.

        Args:
            request: Reading request containing birth data.

        Returns:
            A reading with the eight house placements and a Thaksa summary.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        summary = _summary_from_draw(draw)
        notes = tuple(base.provenance.notes) + (
            "thaksa_cycle=athit-chan-angkhan-phut-sao-pharuehat-rahu-suk",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _summary_from_draw(draw: Draw) -> str:
    common = dict(draw.selections[0].modifiers or {})
    night = " (night)" if common["wednesday_night"] == "true" else ""
    return (
        f"Ruling graha {common['ruler']}{night} "
        f"(color {common['ruler_color']}, strength {common['strength']}, "
        f"{common['buddha_posture']}). Kalakini: {common['kalakini']}."
    )


def build_engine() -> ThaksaEngine:
    """Create a Thaksa engine.

    Returns:
        A new ``ThaksaEngine`` instance.
    """

    return ThaksaEngine()
