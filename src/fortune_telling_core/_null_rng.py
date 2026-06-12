"""Shared RNG sentinel for deterministic engines."""

from fortune_telling_core.errors import ExhaustedRngError


class NullRng:
    kind = "null"

    def __init__(self, message: str) -> None:
        self.message = message

    def randint(self, low: int, high: int) -> int:
        del low, high
        raise ExhaustedRngError(self.message)

    def shuffle(self, n: int) -> list[int]:
        del n
        raise ExhaustedRngError(self.message)

    def random(self) -> float:
        raise ExhaustedRngError(self.message)
