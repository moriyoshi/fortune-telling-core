"""Geomantic shield chart computation.

Four Mothers are generated from random points. The Daughters are the transpose
of the Mothers (the Mothers' rows read as columns); the Nieces, Witnesses, and
Judge follow by geomantic addition, which is bitwise XOR of the four rows. A
classical theorem — used as a test — is that the Judge always has an even number
of points.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.rng import Rng
from fortune_telling_core.traditions.geomancy.figures import Figure, figure_for_rows

_Rows = tuple[int, int, int, int]


def _add(left: _Rows, right: _Rows) -> _Rows:
    combined = tuple(a ^ b for a, b in zip(left, right, strict=True))
    return (combined[0], combined[1], combined[2], combined[3])


def _generate_mothers(rng: Rng) -> list[_Rows]:
    bits = [1 if rng.random() < 0.5 else 0 for _ in range(16)]
    return [(bits[i], bits[i + 1], bits[i + 2], bits[i + 3]) for i in range(0, 16, 4)]


@dataclass(frozen=True, slots=True)
class GeomancyShield:
    """The fifteen figures of a geomantic shield, in reading order."""

    mothers: tuple[Figure, Figure, Figure, Figure]
    daughters: tuple[Figure, Figure, Figure, Figure]
    nieces: tuple[Figure, Figure, Figure, Figure]
    right_witness: Figure
    left_witness: Figure
    judge: Figure


def cast_shield(rng: Rng) -> GeomancyShield:
    """Cast a full geomantic shield from random points.

    Args:
        rng: Random source; sixteen floats are consumed (one per Mother row).

    Returns:
        The completed shield.
    """

    mothers = _generate_mothers(rng)
    daughters = [(mothers[0][j], mothers[1][j], mothers[2][j], mothers[3][j]) for j in range(4)]
    nieces = [
        _add(mothers[0], mothers[1]),
        _add(mothers[2], mothers[3]),
        _add(daughters[0], daughters[1]),
        _add(daughters[2], daughters[3]),
    ]
    right_witness = _add(nieces[0], nieces[1])
    left_witness = _add(nieces[2], nieces[3])
    judge = _add(right_witness, left_witness)

    figures = [figure_for_rows(rows) for rows in (*mothers, *daughters, *nieces)]
    return GeomancyShield(
        mothers=(figures[0], figures[1], figures[2], figures[3]),
        daughters=(figures[4], figures[5], figures[6], figures[7]),
        nieces=(figures[8], figures[9], figures[10], figures[11]),
        right_witness=figure_for_rows(right_witness),
        left_witness=figure_for_rows(left_witness),
        judge=figure_for_rows(judge),
    )
