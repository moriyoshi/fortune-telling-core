import pytest

from fortune_telling_core.traditions.iching.hexagrams import (
    HEXAGRAMS,
    hexagram_for_binary,
)


def test_sixtyfour_hexagrams_numbered_one_to_64() -> None:
    assert [h.number for h in HEXAGRAMS] == list(range(1, 65))


def test_binaries_are_a_bijection_to_0_63() -> None:
    # The strongest table check: every King Wen number maps to a distinct
    # six-bit pattern covering 0..63, so no lower/upper trigram is swapped.
    assert sorted(h.binary for h in HEXAGRAMS) == list(range(64))


@pytest.mark.parametrize(
    ("number", "binary"),
    [
        (1, 0b111111),  # Qian, all yang
        (2, 0b000000),  # Kun, all yin
        (11, 0b000111),  # Tai, Heaven below Earth
        (12, 0b111000),  # Pi, Earth below Heaven
        (29, 0b010010),  # Kan, double Water
        (63, 0b010101),  # Jiji, Fire below Water
        (64, 0b101010),  # Weiji, Water below Fire
    ],
)
def test_known_hexagram_binaries(number: int, binary: int) -> None:
    assert hexagram_for_binary(binary).number == number


def test_glyphs_are_the_yijing_block() -> None:
    assert HEXAGRAMS[0].glyph == "䷀"
    assert HEXAGRAMS[63].glyph == "䷿"
