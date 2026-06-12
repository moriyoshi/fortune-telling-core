"""Celtic tree engine."""

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
from fortune_telling_core.traditions.celtic_tree.birth import parse_birth_data
from fortune_telling_core.traditions.celtic_tree.chart import draw_from_sign
from fortune_telling_core.traditions.celtic_tree.deck import CELTIC_TREE_DECK
from fortune_telling_core.traditions.celtic_tree.signs import classify
from fortune_telling_core.traditions.celtic_tree.spreads import CELTIC_TREE_SPREAD

_NULL_RNG = NullRng("CelticTreeEngine.cast must not use randomness")


class CelticTreeEngine(AbstractEngine):
    """Celtic tree calendar (Ogham tree zodiac) engine.

    The engine deterministically classifies a querent's birth date into one of
    thirteen Ogham tree signs by fixed ``(month, day)`` date ranges. The scheme
    is Robert Graves' 20th-century reconstruction; 23 December (Graves' nameless
    day) is folded into Ruis (Elder) so every date classifies.
    """

    id = "celtic_tree.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the Celtic tree deck.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``CELTIC_TREE_DECK.id``.

        Returns:
            The bundled Celtic tree deck.

        Raises:
            ValidationError: If the requested deck is unsupported.
        """

        if request.deck_id != CELTIC_TREE_DECK.id:
            raise ValidationError(f"unsupported Celtic tree deck: {request.deck_id}")
        return CELTIC_TREE_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the Celtic tree spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``CELTIC_TREE_SPREAD.id``.

        Returns:
            The bundled Celtic tree spread.

        Raises:
            ValidationError: If the requested spread is unsupported.
        """

        if request.spread_id != CELTIC_TREE_SPREAD.id:
            raise ValidationError(f"unsupported Celtic tree spread: {request.spread_id}")
        return CELTIC_TREE_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Classify the birth date into a tree sign as a deterministic draw.

        Args:
            request: Reading request with ``birth_datetime`` in options or
                querent attributes.
            rng: Ignored. The argument is present for ``Engine`` compatibility.

        Returns:
            A draw with the single tree-sign selection.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        del rng
        birth = parse_birth_data(request)
        return draw_from_sign(classify(birth.birth_datetime.date()))

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a Celtic tree reading without a caller RNG.

        Args:
            request: Reading request containing birth data.

        Returns:
            A reading with the tree-sign placement and summary.

        Raises:
            ValidationError: If required birth data is invalid.
        """

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        modifiers = dict(draw.selections[0].modifiers or {})
        summary = (
            f"Celtic tree sign {modifiers['tree']} ({modifiers['ogham']}), "
            f"{modifiers['date_range']}."
        )
        notes = tuple(base.provenance.notes) + (
            "scheme=graves-white-goddess",
            "nameless_day=folded-into-ruis",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def build_engine() -> CelticTreeEngine:
    """Create a Celtic tree engine.

    Returns:
        A new ``CelticTreeEngine`` instance.
    """

    return CelticTreeEngine()
