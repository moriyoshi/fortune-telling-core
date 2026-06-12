import pytest

from fortune_telling_core import ExhaustedRngError, RandomRng, SequenceRng, ValidationError


def test_random_rng_is_deterministic_for_seed() -> None:
    first = RandomRng(1234)
    second = RandomRng(1234)

    assert first.shuffle(8) == second.shuffle(8)
    assert first.randint(1, 10) == second.randint(1, 10)
    assert first.random() == second.random()


def test_random_rng_fisher_yates_stability() -> None:
    assert RandomRng(42).shuffle(10) == [7, 3, 2, 8, 5, 6, 9, 4, 0, 1]


def test_sequence_rng_replays_values_and_exhausts() -> None:
    rng = SequenceRng(ints=[2, 0, 1, 4], floats=[0.25])

    assert rng.shuffle(3) == [2, 0, 1]
    assert rng.randint(1, 5) == 4
    assert rng.random() == 0.25
    with pytest.raises(ExhaustedRngError):
        rng.random()


def test_sequence_rng_validates_shuffle_permutation() -> None:
    with pytest.raises(ValidationError):
        SequenceRng(ints=[0, 0]).shuffle(2)
