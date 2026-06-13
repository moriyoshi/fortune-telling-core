import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_values import latin_pythagorean
from fortune_telling_core.traditions._name_values.latin_pythagorean import (
    LETTER_VALUES,
    NormalizationMode,
)


def test_letter_value_anchors() -> None:
    assert LETTER_VALUES["A"] == 1
    assert LETTER_VALUES["I"] == 9
    assert LETTER_VALUES["J"] == 1
    assert LETTER_VALUES["R"] == 9
    assert LETTER_VALUES["S"] == 1
    assert LETTER_VALUES["Z"] == 8


def test_values_fold_case_and_ignore_non_letters() -> None:
    units = latin_pythagorean.values("Jo-hn 1!")
    assert [(unit.char, unit.value) for unit in units] == [
        ("J", 1),
        ("O", 6),
        ("H", 8),
        ("N", 5),
    ]


def test_values_empty_when_no_letters() -> None:
    assert latin_pythagorean.values("123 ...") == ()


def test_accent_fold_maps_decomposable_latin_letters() -> None:
    units = latin_pythagorean.values(
        "José",
        normalization=NormalizationMode.LATIN_ACCENT_FOLD,
    )
    assert [(unit.char, unit.value) for unit in units] == [
        ("J", 1),
        ("O", 6),
        ("S", 1),
        ("E", 5),
    ]


def test_accent_fold_rejects_unmapped_meaningful_characters() -> None:
    with pytest.raises(ValidationError):
        latin_pythagorean.values("Søren", normalization=NormalizationMode.LATIN_ACCENT_FOLD)


def test_stable_id_and_version() -> None:
    assert latin_pythagorean.ID == "latin_pythagorean.v1"
    assert latin_pythagorean.VERSION == "1"
