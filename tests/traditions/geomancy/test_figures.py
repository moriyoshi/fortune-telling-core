import pytest

from fortune_telling_core.traditions.geomancy.figures import (
    FIGURE_BY_SLUG,
    FIGURES,
)


def test_sixteen_figures_bijection_to_0_15() -> None:
    # The strongest table check: each figure maps to a distinct 4-bit value
    # covering 0..15, so no row pattern is duplicated or transposed.
    assert sorted(figure.value for figure in FIGURES) == list(range(16))


@pytest.mark.parametrize(
    ("slug", "rows"),
    [
        ("via", (1, 1, 1, 1)),
        ("populus", (0, 0, 0, 0)),
        ("carcer", (1, 0, 0, 1)),
        ("coniunctio", (0, 1, 1, 0)),
        ("albus", (0, 0, 1, 0)),  # Earth-on-Water
    ],
)
def test_anchor_figures(slug: str, rows: tuple[int, int, int, int]) -> None:
    assert FIGURE_BY_SLUG[slug].rows == rows


@pytest.mark.parametrize(
    ("first", "second"),
    [
        ("puer", "puella"),
        ("caput_draconis", "cauda_draconis"),
        ("albus", "rubeus"),
        ("laetitia", "tristitia"),
        ("amissio", "acquisitio"),
    ],
)
def test_inversion_pairs(first: str, second: str) -> None:
    # Turning a figure upside down reverses its rows.
    a = FIGURE_BY_SLUG[first].rows
    b = FIGURE_BY_SLUG[second].rows
    assert tuple(reversed(a)) == b


def test_ruling_element_from_top_rows() -> None:
    assert FIGURE_BY_SLUG["via"].ruling_element == "fire"
    assert FIGURE_BY_SLUG["populus"].ruling_element == "earth"
    assert FIGURE_BY_SLUG["caput_draconis"].ruling_element == "air"
    assert FIGURE_BY_SLUG["puella"].ruling_element == "water"
