"""I Ching line casting via the three-coin method."""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.rng import Rng
from fortune_telling_core.traditions.iching.hexagrams import Hexagram, hexagram_for_binary

_LINES = 6
_COINS = 3


@dataclass(frozen=True, slots=True)
class CastLine:
    """A single cast line."""

    value: int
    """Coin total: 6 (old yin), 7 (young yang), 8 (young yin), 9 (old yang)."""

    @property
    def yang(self) -> bool:
        return self.value % 2 == 1

    @property
    def changing(self) -> bool:
        return self.value in (6, 9)


@dataclass(frozen=True, slots=True)
class Casting:
    """The six cast lines and the hexagrams they yield."""

    lines: tuple[CastLine, ...]

    @property
    def primary(self) -> Hexagram:
        binary = sum(int(line.yang) << index for index, line in enumerate(self.lines))
        return hexagram_for_binary(binary)

    @property
    def relating(self) -> Hexagram:
        binary = sum(
            int(line.yang ^ line.changing) << index for index, line in enumerate(self.lines)
        )
        return hexagram_for_binary(binary)

    @property
    def changing_positions(self) -> tuple[int, ...]:
        """1-based positions (bottom = 1) of the changing lines."""

        return tuple(index + 1 for index, line in enumerate(self.lines) if line.changing)


def cast(rng: Rng) -> Casting:
    """Cast six lines bottom-to-top with the three-coin method.

    Each coin lands heads (3) or tails (2) with equal probability; the line is
    the sum of three coins, giving the 6/7/8/9 distribution.

    Args:
        rng: Random source; three floats are consumed per line.

    Returns:
        The completed casting.
    """

    lines = [
        CastLine(sum(3 if rng.random() < 0.5 else 2 for _ in range(_COINS))) for _ in range(_LINES)
    ]
    return Casting(tuple(lines))
