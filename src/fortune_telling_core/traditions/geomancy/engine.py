"""Western geomancy engine."""

from __future__ import annotations

from dataclasses import replace

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions.geomancy.deck import GEOMANCY_DECK
from fortune_telling_core.traditions.geomancy.shield import GeomancyShield, cast_shield
from fortune_telling_core.traditions.geomancy.spreads import SHIELD


class GeomancyEngine(AbstractEngine):
    """Western geomancy engine.

    Four Mother figures are generated from random points, then the Daughters,
    Nieces, two Witnesses, and the Judge are derived deterministically by
    geomantic addition. The fifteen figures fill the shield spread.
    """

    id = "geomancy.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the geomancy figure deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``GEOMANCY_DECK.id``.

        Returns:
            The bundled geomancy deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != GEOMANCY_DECK.id:
            raise ValidationError(f"unsupported geomancy deck: {request.deck_id}")
        return GEOMANCY_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the shield spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``SHIELD.id``.

        Returns:
            The bundled shield spread.

        Raises:
            ValidationError: If the spread is not supported.
        """

        if request.spread_id != SHIELD.id:
            raise ValidationError(f"unsupported geomancy spread: {request.spread_id}")
        return SHIELD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Cast a geomantic shield for the request.

        Args:
            request: Reading request.
            rng: Random source; sixteen floats are consumed (one per Mother
                row).

        Returns:
            A draw with the fifteen shield selections in reading order.

        Raises:
            ValidationError: If the requested deck or spread is unsupported.
            ExhaustedRngError: If the supplied RNG cannot provide enough values.
        """

        self.deck(request)
        spread = self.spread(request)
        shield = cast_shield(rng)
        figures = (
            *shield.mothers,
            *shield.daughters,
            *shield.nieces,
            shield.right_witness,
            shield.left_witness,
            shield.judge,
        )
        common = _common_modifiers(shield)
        selections = tuple(
            Selection(
                position_id=position.id,
                symbol_id=figure.symbol_id,
                modifiers={
                    **common,
                    "role": position.id,
                    "figure": figure.name,
                    "element": figure.ruling_element,
                },
            )
            for position, figure in zip(spread.positions, figures, strict=True)
        )
        return Draw(deck_id=GEOMANCY_DECK.id, spread_id=SHIELD.id, selections=selections)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[-1].modifiers or {})
        summary = (
            f"Judge: {modifiers['judge']}. "
            f"Witnesses: {modifiers['right_witness']} (right), "
            f"{modifiers['left_witness']} (left)."
        )
        return replace(base, summary=summary)


def _common_modifiers(shield: GeomancyShield) -> dict[str, str]:
    return {
        "judge": shield.judge.name,
        "right_witness": shield.right_witness.name,
        "left_witness": shield.left_witness.name,
    }


def build_engine() -> GeomancyEngine:
    """Create a Western geomancy engine.

    Returns:
        A new ``GeomancyEngine`` instance.
    """

    return GeomancyEngine()
