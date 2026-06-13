import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_values import greek_isopsephy
from fortune_telling_core.traditions._name_values.greek_isopsephy import SigmaMode


def _total(
    name: str,
    *,
    sigma_mode: SigmaMode = SigmaMode.FINAL_TO_SIGMA,
) -> int:
    return greek_isopsephy.total(greek_isopsephy.values(name, sigma_mode=sigma_mode))


def test_letter_value_anchors() -> None:
    assert _total("α") == 1
    assert _total("θ") == 9
    assert _total("ι") == 10
    assert _total("ξ") == 60
    assert _total("ρ") == 100
    assert _total("ω") == 800


def test_obsolete_numeric_letters() -> None:
    assert _total("ϝ") == 6
    assert _total("ϛ") == 6
    assert _total("ϙ") == 90
    assert _total("ϟ") == 90
    assert _total("ϡ") == 900


def test_diacritics_and_punctuation_ignored() -> None:
    assert _total("Ἀλέξανδρος") == _total("Αλεξανδρος")
    assert _total("Αλέξανδρος!") == _total("Αλεξανδρος")


def test_final_sigma_normalized_by_default() -> None:
    units = greek_isopsephy.values("λόγος")
    assert units[-1].char == "σ"
    assert _total("ς") == _total("σ")


def test_final_sigma_can_remain_distinct() -> None:
    units = greek_isopsephy.values("ς", sigma_mode=SigmaMode.DISTINCT)
    assert [(unit.char, unit.value) for unit in units] == [("ς", 200)]


@pytest.mark.parametrize("name", ["John", "שלום", "山田"])
def test_rejects_unsupported_letters(name: str) -> None:
    with pytest.raises(ValidationError):
        greek_isopsephy.values(name)


def test_stable_id_and_version() -> None:
    assert greek_isopsephy.ID == "greek_isopsephy.v1"
    assert greek_isopsephy.VERSION == "1"
