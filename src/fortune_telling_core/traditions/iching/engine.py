"""I Ching engine."""

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
from fortune_telling_core.traditions.iching.cast import Casting, cast
from fortune_telling_core.traditions.iching.deck import ICHING_DECK
from fortune_telling_core.traditions.iching.spreads import CASTING


class IChingEngine(AbstractEngine):
    """I Ching engine using the three-coin casting method.

    The engine casts six lines to build a primary hexagram and, by transforming
    the changing lines (old yin and old yang), a relating hexagram. When no line
    changes, the relating hexagram equals the primary.
    """

    id = "iching.engine"
    version = "0.1.0"

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the hexagram deck for a request.

        Args:
            request: Reading request whose ``deck_id`` must match
                ``ICHING_DECK.id``.

        Returns:
            The bundled hexagram deck.

        Raises:
            ValidationError: If the request names an unsupported deck.
        """

        if request.deck_id != ICHING_DECK.id:
            raise ValidationError(f"unsupported I Ching deck: {request.deck_id}")
        return ICHING_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the casting spread.

        Args:
            request: Reading request whose ``spread_id`` must match
                ``CASTING.id``.

        Returns:
            The bundled casting spread.

        Raises:
            ValidationError: If the spread is not supported.
        """

        if request.spread_id != CASTING.id:
            raise ValidationError(f"unsupported I Ching spread: {request.spread_id}")
        return CASTING

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Cast a hexagram for the request.

        Args:
            request: Reading request.
            rng: Random source; eighteen floats are consumed (three coins per
                line).

        Returns:
            A draw with the primary and relating hexagram selections.

        Raises:
            ValidationError: If the requested deck or spread is unsupported.
            ExhaustedRngError: If the supplied RNG cannot provide enough values.
        """

        self.deck(request)
        self.spread(request)
        casting = cast(rng)
        common = _common_modifiers(casting)
        selections = (
            Selection("primary", casting.primary.symbol_id, {**common, "role": "primary"}),
            Selection("relating", casting.relating.symbol_id, {**common, "role": "relating"}),
        )
        return Draw(ICHING_DECK.id, CASTING.id, selections)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        return replace(base, summary=_summary_from_draw(draw))


def _common_modifiers(casting: Casting) -> dict[str, str]:
    primary = casting.primary
    relating = casting.relating
    return {
        "lines": ",".join(str(line.value) for line in casting.lines),
        "changing_lines": ",".join(str(position) for position in casting.changing_positions),
        "primary": str(primary.number),
        "primary_name": primary.pinyin,
        "relating": str(relating.number),
        "relating_name": relating.pinyin,
    }


def _summary_from_draw(draw: Draw) -> str:
    modifiers = dict(draw.selections[0].modifiers or {})
    primary = f"Primary hexagram {modifiers['primary']} {modifiers['primary_name']}"
    changing = modifiers["changing_lines"]
    if not changing:
        return f"{primary}; no changing lines."
    return (
        f"{primary}; changing lines {changing.replace(',', ', ')} → "
        f"relating hexagram {modifiers['relating']} {modifiers['relating_name']}."
    )


def build_engine() -> IChingEngine:
    """Create an I Ching engine.

    Returns:
        A new ``IChingEngine`` instance.
    """

    return IChingEngine()
