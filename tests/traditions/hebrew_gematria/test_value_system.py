import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_values import hebrew_gematria
from fortune_telling_core.traditions._name_values.hebrew_gematria import FinalLetterMode


def _total(name: str, **kwargs: FinalLetterMode) -> int:
    return hebrew_gematria.total(hebrew_gematria.values(name, **kwargs))


def test_letter_value_anchors() -> None:
    # alef=1, yod=10, kaf=20, qof=100, tav=400.
    assert _total("א") == 1
    assert _total("י") == 10
    assert _total("כ") == 20
    assert _total("ק") == 100
    assert _total("ת") == 400


def test_standard_final_forms_share_base_value() -> None:
    # final mem == mem == 40.
    assert _total("ם") == 40
    assert _total("מ") == 40


def test_gadol_final_forms_use_500_to_900() -> None:
    assert _total("ם", final_letter_mode=FinalLetterMode.GADOL) == 600
    assert _total("ך", final_letter_mode=FinalLetterMode.GADOL) == 500
    assert _total("ץ", final_letter_mode=FinalLetterMode.GADOL) == 900
    # Base (non-final) letters are unaffected by gadol mode.
    assert _total("מ", final_letter_mode=FinalLetterMode.GADOL) == 40


def test_niqqud_and_whitespace_ignored() -> None:
    assert _total("שָׁלוֹם") == _total("שלום")
    assert _total("בן אדם") == _total("בןאדם")


def test_value_trace_order_preserved() -> None:
    units = hebrew_gematria.values("חיים")
    assert [(unit.char, unit.value) for unit in units] == [
        ("ח", 8),
        ("י", 10),
        ("י", 10),
        ("ם", 40),
    ]


@pytest.mark.parametrize("name", ["John", "Δabc", "山田"])
def test_rejects_unsupported_letters(name: str) -> None:
    with pytest.raises(ValidationError):
        hebrew_gematria.values(name)


def test_stable_id_and_version() -> None:
    assert hebrew_gematria.ID == "hebrew_gematria.v1"
    assert hebrew_gematria.VERSION == "1"
