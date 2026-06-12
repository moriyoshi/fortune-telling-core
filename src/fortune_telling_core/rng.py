"""Randomness boundary for reproducible readings."""

from __future__ import annotations

import random
from collections.abc import Iterable
from typing import Protocol

from fortune_telling_core.errors import ExhaustedRngError, ValidationError


class Rng(Protocol):
    """Narrow RNG protocol used by engines.

    Engines depend on this small protocol rather than `random.Random` directly
    so tests can inject deterministic replay streams.
    """

    def randint(self, low: int, high: int) -> int:
        """Return an integer in the inclusive range `[low, high]`.

        Args:
            low: Inclusive lower bound.
            high: Inclusive upper bound.

        Returns:
            An integer within the requested range.
        """

    def shuffle(self, n: int) -> list[int]:
        """Return a permutation of `range(n)`.

        Args:
            n: Number of indices to permute.

        Returns:
            A list containing each integer from `0` to `n - 1` exactly once.
        """

    def random(self) -> float:
        """Return a float in the half-open interval `[0.0, 1.0)`."""


class RandomRng:
    """Seeded RNG with an explicit Fisher-Yates implementation.

    Args:
        seed: Seed passed to `random.Random`.

    Example:
        ```python
        from fortune_telling_core import RandomRng

        rng = RandomRng(42)
        order = rng.shuffle(3)
        ```
    """

    kind = "random"

    def __init__(self, seed: int | str | bytes | bytearray | None = None) -> None:
        self.seed = seed
        self._random = random.Random(seed)

    def randint(self, low: int, high: int) -> int:
        """Return an inclusive random integer.

        Args:
            low: Inclusive lower bound.
            high: Inclusive upper bound.

        Returns:
            A random integer in the requested range.

        Raises:
            ValidationError: If `high` is lower than `low`.
        """

        if high < low:
            raise ValidationError("high must be greater than or equal to low")
        return self._random.randrange(low, high + 1)

    def shuffle(self, n: int) -> list[int]:
        """Return a deterministic Fisher-Yates permutation.

        Args:
            n: Number of indices to permute.

        Returns:
            A permutation of `range(n)`.

        Raises:
            ValidationError: If `n` is negative.
        """

        if n < 0:
            raise ValidationError("shuffle length must be non-negative")
        values = list(range(n))
        for index in range(n - 1, 0, -1):
            swap_index = self._random.randrange(index + 1)
            values[index], values[swap_index] = values[swap_index], values[index]
        return values

    def random(self) -> float:
        """Return the next float from the underlying seeded generator."""

        return self._random.random()


class SequenceRng:
    """Replay/test RNG backed by fixed integer and float sequences.

    Args:
        ints: Integer values consumed by `randint` and `shuffle`.
        floats: Float values consumed by `random`.

    Example:
        ```python
        from fortune_telling_core import SequenceRng

        rng = SequenceRng(ints=[2, 0, 1], floats=[0.25])
        assert rng.shuffle(3) == [2, 0, 1]
        ```
    """

    kind = "sequence"

    def __init__(
        self,
        ints: Iterable[int] = (),
        floats: Iterable[float] = (),
    ) -> None:
        self._ints = list(ints)
        self._floats = list(floats)
        self._int_index = 0
        self._float_index = 0

    def _next_int(self) -> int:
        if self._int_index >= len(self._ints):
            raise ExhaustedRngError("integer RNG sequence is exhausted")
        value = self._ints[self._int_index]
        self._int_index += 1
        return value

    def randint(self, low: int, high: int) -> int:
        """Return the next integer from the replay sequence.

        Args:
            low: Inclusive lower bound.
            high: Inclusive upper bound.

        Returns:
            The next integer.

        Raises:
            ExhaustedRngError: If no integer values remain.
            ValidationError: If bounds are invalid or the next value is outside
                the requested range.
        """

        if high < low:
            raise ValidationError("high must be greater than or equal to low")
        value = self._next_int()
        if value < low or value > high:
            raise ValidationError(f"integer RNG value {value} is outside [{low}, {high}]")
        return value

    def shuffle(self, n: int) -> list[int]:
        """Consume `n` integers as an explicit permutation.

        Args:
            n: Number of indices to consume.

        Returns:
            The next `n` integers.

        Raises:
            ExhaustedRngError: If fewer than `n` integers remain.
            ValidationError: If `n` is negative or values are not a permutation
                of `range(n)`.
        """

        if n < 0:
            raise ValidationError("shuffle length must be non-negative")
        values = [self._next_int() for _ in range(n)]
        if sorted(values) != list(range(n)):
            raise ValidationError("shuffle sequence must be a permutation of range(n)")
        return values

    def random(self) -> float:
        """Return the next float from the replay sequence.

        Returns:
            The next float.

        Raises:
            ExhaustedRngError: If no float values remain.
            ValidationError: If the next value is outside `[0.0, 1.0)`.
        """

        if self._float_index >= len(self._floats):
            raise ExhaustedRngError("float RNG sequence is exhausted")
        value = self._floats[self._float_index]
        self._float_index += 1
        if value < 0.0 or value >= 1.0:
            raise ValidationError("float RNG value must be in [0.0, 1.0)")
        return value
