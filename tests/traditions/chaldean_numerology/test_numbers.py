from string import ascii_uppercase

import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions.chaldean_numerology.numbers import (
    _LETTER_VALUES,
    compute_name_number,
    number,
    reduce_to_root,
)


def test_all_26_letters_mapped_to_1_through_8() -> None:
    assert set(_LETTER_VALUES) == set(ascii_uppercase)
    assert set(_LETTER_VALUES.values()) == {1, 2, 3, 4, 5, 6, 7, 8}  # never 9


@pytest.mark.parametrize(("total", "root"), [(18, 9), (23, 5), (10, 1), (9, 9), (48, 3)])
def test_reduce_to_root(total: int, root: int) -> None:
    assert reduce_to_root(total) == root


def test_known_name_number() -> None:
    result = compute_name_number("John")  # J1 + O7 + H5 + N5 = 18 -> 9

    assert (result.total, result.root) == (18, 9)
    assert number(result.root).planet == "Mars"


def test_non_letters_ignored() -> None:
    assert compute_name_number("J.O.H.N") == compute_name_number("John")


def test_planetary_rulers() -> None:
    assert number(1).planet == "Sun"
    assert number(8).planet == "Saturn"


def test_errors_on_letterless_name() -> None:
    with pytest.raises(ValidationError):
        compute_name_number("123 ---")
