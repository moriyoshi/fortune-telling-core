"""Double-six domino set as generic data.

A double-six set is the 28 unordered pairs of pip counts from 0 to 6 — pure
combinatorics, so the deck is certain. Domino divination traditionally draws one
to three tiles; here the tiles are exposed as a deck for the engine to shuffle.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DominoTile:
    """One domino: two pip counts, ``high`` >= ``low``."""

    high: int
    low: int

    @property
    def pips(self) -> int:
        return self.high + self.low

    @property
    def double(self) -> bool:
        return self.high == self.low

    @property
    def slug(self) -> str:
        return f"{self.high}_{self.low}"

    @property
    def name(self) -> str:
        return f"{self.high}-{self.low}"

    @property
    def symbol_id(self) -> str:
        return f"dominoes.tile.{self.slug}"


TILES: tuple[DominoTile, ...] = tuple(
    DominoTile(high, low) for high in range(7) for low in range(high + 1)
)
