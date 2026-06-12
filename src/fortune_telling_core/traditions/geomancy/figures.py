"""The sixteen geomantic figures.

Each figure has four rows — Fire, Air, Water, Earth from top to bottom — where a
row is either a single point (active, 1) or a double point (passive, 0). The
four-bit value (Fire as the most significant bit) gives a bijection between the
figures and 0..15, checked in the tests.

The table is cross-checked several ways: the top two rows place each figure in
one of four elemental groups (matching the published grouping), the classic
inversion pairs (Puer/Puella, Caput/Cauda Draconis, Albus/Rubeus,
Laetitia/Tristitia, Amissio/Acquisitio) hold, and the anchor figures Via, Populus,
Carcer, Coniunctio, and Albus match.
"""

from __future__ import annotations

from dataclasses import dataclass

_RULING_ELEMENT = {(1, 1): "fire", (0, 1): "air", (1, 0): "water", (0, 0): "earth"}


@dataclass(frozen=True, slots=True)
class Figure:
    """One geomantic figure."""

    slug: str
    name: str
    english: str
    rows: tuple[int, int, int, int]
    """Fire, Air, Water, Earth; 1 for a single (active) point, 0 for double."""

    @property
    def value(self) -> int:
        fire, air, water, earth = self.rows
        return (fire << 3) | (air << 2) | (water << 1) | earth

    @property
    def ruling_element(self) -> str:
        return _RULING_ELEMENT[(self.rows[0], self.rows[1])]

    @property
    def points(self) -> int:
        """Total points (single = 1, double = 2)."""

        return sum(1 if row else 2 for row in self.rows)

    @property
    def symbol_id(self) -> str:
        return f"geomancy.figure.{self.slug}"


FIGURES: tuple[Figure, ...] = (
    Figure("via", "Via", "The Way", (1, 1, 1, 1)),
    Figure("cauda_draconis", "Cauda Draconis", "Dragon's Tail", (1, 1, 1, 0)),
    Figure("puer", "Puer", "Boy", (1, 1, 0, 1)),
    Figure("fortuna_minor", "Fortuna Minor", "Lesser Fortune", (1, 1, 0, 0)),
    Figure("caput_draconis", "Caput Draconis", "Dragon's Head", (0, 1, 1, 1)),
    Figure("coniunctio", "Coniunctio", "Conjunction", (0, 1, 1, 0)),
    Figure("acquisitio", "Acquisitio", "Gain", (0, 1, 0, 1)),
    Figure("rubeus", "Rubeus", "Red", (0, 1, 0, 0)),
    Figure("puella", "Puella", "Girl", (1, 0, 1, 1)),
    Figure("amissio", "Amissio", "Loss", (1, 0, 1, 0)),
    Figure("carcer", "Carcer", "Prison", (1, 0, 0, 1)),
    Figure("laetitia", "Laetitia", "Joy", (1, 0, 0, 0)),
    Figure("fortuna_maior", "Fortuna Maior", "Greater Fortune", (0, 0, 1, 1)),
    Figure("albus", "Albus", "White", (0, 0, 1, 0)),
    Figure("tristitia", "Tristitia", "Sorrow", (0, 0, 0, 1)),
    Figure("populus", "Populus", "People", (0, 0, 0, 0)),
)

FIGURE_BY_ROWS = {figure.rows: figure for figure in FIGURES}
FIGURE_BY_SLUG = {figure.slug: figure for figure in FIGURES}


def figure_for_rows(rows: tuple[int, int, int, int]) -> Figure:
    """Return the figure for a four-row pattern."""

    return FIGURE_BY_ROWS[rows]
