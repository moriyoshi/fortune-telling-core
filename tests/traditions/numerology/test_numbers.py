from datetime import date

import pytest

from fortune_telling_core.traditions.numerology.config import ReductionMethod
from fortune_telling_core.traditions.numerology.numbers import compute_chart, reduce_number


@pytest.mark.parametrize(
    ("value", "expected"),
    [(8, 8), (10, 1), (28, 1), (11, 11), (22, 22), (33, 33), (29, 11), (1987, 7)],
)
def test_reduce_number_preserves_masters(value: int, expected: int) -> None:
    assert reduce_number(value) == expected


def test_component_life_path_and_birthday() -> None:
    chart = compute_chart(date(1987, 8, 17), ReductionMethod.COMPONENT)

    assert chart.life_path == 5
    assert chart.birthday == 8


def test_birthday_keeps_master_number() -> None:
    # The 29th reduces to 11, a master number.
    assert compute_chart(date(1990, 11, 29), ReductionMethod.COMPONENT).birthday == 11


def test_methods_diverge_on_master_number() -> None:
    component = compute_chart(date(1985, 9, 1), ReductionMethod.COMPONENT)
    iterative = compute_chart(date(1985, 9, 1), ReductionMethod.ITERATIVE)

    assert component.life_path == 6
    assert iterative.life_path == 33  # iterative preserves the master number here


def test_methods_agree_when_no_master_surfaces() -> None:
    for birth in (date(1987, 8, 17), date(2000, 1, 1), date(1980, 12, 25)):
        component = compute_chart(birth, ReductionMethod.COMPONENT).life_path
        iterative = compute_chart(birth, ReductionMethod.ITERATIVE).life_path
        assert component == iterative
