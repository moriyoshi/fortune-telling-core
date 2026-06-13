import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_values import cyrillic_pythagorean
from fortune_telling_core.traditions._name_values.cyrillic_pythagorean import (
    Alphabet,
    Language,
    NormalizationMode,
    ShortIMode,
    SignsMode,
    YoMode,
)


def _total(
    name: str,
    *,
    language: Language = Language.RUSSIAN,
    alphabet: Alphabet | None = None,
    yo_mode: YoMode = YoMode.DISTINCT,
    signs_mode: SignsMode = SignsMode.COUNT,
    short_i_mode: ShortIMode = ShortIMode.DISTINCT,
    normalization: NormalizationMode = NormalizationMode.STRICT_CYRILLIC,
) -> int:
    return cyrillic_pythagorean.total(
        cyrillic_pythagorean.values(
            name,
            language=language,
            alphabet=alphabet,
            yo_mode=yo_mode,
            signs_mode=signs_mode,
            short_i_mode=short_i_mode,
            normalization=normalization,
        )
    )


def test_russian_33_letter_value_anchors() -> None:
    assert _total("а") == 1
    assert _total("з") == 9
    assert _total("и") == 1
    assert _total("ё") == 7
    assert _total("я") == 6


def test_russian_32_no_yo_requires_explicit_yo_fold() -> None:
    with pytest.raises(ValidationError):
        cyrillic_pythagorean.values("ёлка", alphabet=Alphabet.RUSSIAN_32_NO_YO)
    units = cyrillic_pythagorean.values(
        "ёлка",
        alphabet=Alphabet.RUSSIAN_32_NO_YO,
        yo_mode=YoMode.FOLD_TO_E,
    )
    assert units[0].char == "е"


def test_sign_and_short_i_options_are_explicit() -> None:
    assert _total("й") == 2
    assert _total("й", short_i_mode=ShortIMode.FOLD_TO_I) == 1
    assert (
        cyrillic_pythagorean.values(
            "ъь",
            signs_mode=SignsMode.IGNORE_HARD_SOFT_SIGNS,
        )
        == ()
    )


def test_other_language_tables() -> None:
    assert _total("ї", language=Language.UKRAINIAN) == 4
    assert _total("ђ", language=Language.SERBIAN) == 6
    assert _total("щ", language=Language.BULGARIAN) == 8


@pytest.mark.parametrize("name", ["John", "שלום", "山田"])
def test_rejects_unsupported_letters(name: str) -> None:
    with pytest.raises(ValidationError):
        cyrillic_pythagorean.values(name)


def test_rejects_incompatible_language_and_alphabet() -> None:
    with pytest.raises(ValidationError):
        cyrillic_pythagorean.values(
            "иван",
            language=Language.UKRAINIAN,
            alphabet=Alphabet.RUSSIAN_33,
        )


def test_stable_id_and_version() -> None:
    assert cyrillic_pythagorean.ID == "cyrillic_pythagorean.v1"
    assert cyrillic_pythagorean.VERSION == "1"
