"""Engine contracts and default structural reading plumbing."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, cast

import fortune_telling_core
from fortune_telling_core.draw import Draw
from fortune_telling_core.errors import UnknownSymbolError, ValidationError
from fortune_telling_core.provenance import Provenance
from fortune_telling_core.reading import PositionReading, Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.serde import SCHEMA_VERSION
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck


class Engine(Protocol):
    """Protocol implemented by all reading engines."""

    id: str
    version: str

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the deck for `request`.

        Args:
            request: Reading request.

        Returns:
            Deck selected by the request.
        """

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the spread for `request`."""

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Create a fully determined draw."""

    def interpret(self, request: ReadingRequest, draw: Draw) -> Reading:
        """Resolve a recorded draw without using randomness."""

    def read(self, request: ReadingRequest, *, rng: Rng) -> Reading:
        """Draw and resolve a reading."""

    def replay(self, request: ReadingRequest, draw: Draw) -> Reading:
        """Resolve a recorded draw without using randomness."""


class AbstractEngine(ABC):
    """Base class supplying common read, replay, and structural reading plumbing."""

    id: str
    version: str

    @abstractmethod
    def deck(self, request: ReadingRequest) -> Deck:
        """Return the deck for `request`."""

    @abstractmethod
    def spread(self, request: ReadingRequest) -> Spread:
        """Return the spread for `request`."""

    @abstractmethod
    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Create a fully determined draw."""

    def read(self, request: ReadingRequest, *, rng: Rng) -> Reading:
        """Draw and resolve a reading.

        Args:
            request: Reading request.
            rng: Random number generator used by `draw`.

        Returns:
            The structural reading.

        Raises:
            ValidationError: If request, draw, deck, or spread data is
                inconsistent.
            UnknownSymbolError: If the draw references a symbol absent from the
                deck.
        """

        draw = self.draw(request, rng)
        return self._interpret(request, draw, rng=rng)

    def replay(self, request: ReadingRequest, draw: Draw) -> Reading:
        """Resolve a recorded draw without using randomness.

        Args:
            request: Reading request matching the draw.
            draw: Recorded draw to resolve.

        Returns:
            The structural reading.
        """

        return self._interpret(request, draw, rng=None)

    def interpret(self, request: ReadingRequest, draw: Draw) -> Reading:
        """Alias for `replay`.

        Args:
            request: Reading request matching the draw.
            draw: Recorded draw to resolve.

        Returns:
            The structural reading.
        """

        return self.replay(request, draw)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        deck = self.deck(request)
        spread = self.spread(request)
        if draw.deck_id != deck.id:
            raise ValidationError(f"draw deck_id {draw.deck_id!r} does not match deck {deck.id!r}")
        if draw.spread_id != spread.id:
            raise ValidationError(
                f"draw spread_id {draw.spread_id!r} does not match spread {spread.id!r}"
            )
        if len(draw.selections) != spread.size:
            raise ValidationError("draw selection count must match spread size")

        expected_positions = tuple(position.id for position in spread.positions)
        actual_positions = tuple(selection.position_id for selection in draw.selections)
        if actual_positions != expected_positions:
            raise ValidationError("draw selections must be ordered by spread position")

        position_readings: list[PositionReading] = []
        for position, selection in zip(spread.positions, draw.selections, strict=True):
            symbol = deck.symbol_by_id(selection.symbol_id)
            if symbol is None:
                raise UnknownSymbolError(f"unknown symbol id: {selection.symbol_id}")
            position_readings.append(PositionReading(position, symbol, selection))

        return Reading(
            request=request,
            spread=spread,
            draw=draw,
            positions=tuple(position_readings),
            summary=None,
            provenance=self._provenance(request, deck, spread, rng),
            schema_version=SCHEMA_VERSION,
        )

    def _provenance(
        self,
        request: ReadingRequest,
        deck: Deck,
        spread: Spread,
        rng: Rng | None,
    ) -> Provenance:
        rng_kind = None if rng is None else getattr(rng, "kind", type(rng).__name__)
        raw_seed = None if rng is None else getattr(rng, "seed", None)
        return Provenance(
            engine_id=self.id,
            engine_version=self.version,
            library_version=fortune_telling_core.__version__,
            deck_id=deck.id,
            spread_id=spread.id,
            rng_kind=cast(str | None, rng_kind),
            rng_seed=None if raw_seed is None else str(raw_seed),
            created_at=request.requested_at,
        )
