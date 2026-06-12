import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions.name_numerology.compute import compute_chart
from fortune_telling_core.traditions.name_numerology.config import YMode


def test_known_name_core_numbers() -> None:
    chart = compute_chart("John", YMode.CONSONANT)

    assert (chart.expression, chart.soul_urge, chart.personality) == (2, 6, 5)


def test_y_mode_changes_vowel_and_consonant_numbers() -> None:
    consonant = compute_chart("Amy", YMode.CONSONANT)
    vowel = compute_chart("Amy", YMode.VOWEL)

    # Expression is unaffected (all letters either way).
    assert consonant.expression == vowel.expression == 3
    # As a consonant, Y joins M to make a master-number Personality.
    assert (consonant.soul_urge, consonant.personality) == (1, 11)
    # As a vowel, Y joins A in the Soul Urge instead.
    assert (vowel.soul_urge, vowel.personality) == (8, 4)


def test_non_letters_are_ignored() -> None:
    assert compute_chart("J.O.H.N!", YMode.CONSONANT) == compute_chart("John", YMode.CONSONANT)


def test_errors_on_empty_or_vowelless_name() -> None:
    with pytest.raises(ValidationError):
        compute_chart("123", YMode.CONSONANT)
    with pytest.raises(ValidationError):
        compute_chart("Lynn", YMode.CONSONANT)  # no base vowel, Y is a consonant here
