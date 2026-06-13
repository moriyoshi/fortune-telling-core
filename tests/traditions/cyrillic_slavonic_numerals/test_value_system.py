import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_values import cyrillic_slavonic_numerals
from fortune_telling_core.traditions._name_values.cyrillic_slavonic_numerals import (
    KoppaMode,
    LetterTable,
    Omega800Mode,
    TitloMode,
    U400Mode,
    UnvaluedLettersMode,
    XiMode,
)


def _total(
    name: str,
    *,
    letter_table: LetterTable = LetterTable.COMMON_CHURCH_SLAVONIC,
    koppa_mode: KoppaMode = KoppaMode.CHERV_90,
    xi_mode: XiMode = XiMode.KSI_60,
    u_400_mode: U400Mode = U400Mode.UK,
    omega_800_mode: Omega800Mode = Omega800Mode.OMEGA,
    unvalued_letters: UnvaluedLettersMode = UnvaluedLettersMode.REJECT,
    titlo: TitloMode = TitloMode.OPTIONAL,
) -> int:
    return cyrillic_slavonic_numerals.total(
        cyrillic_slavonic_numerals.values(
            name,
            letter_table=letter_table,
            koppa_mode=koppa_mode,
            xi_mode=xi_mode,
            u_400_mode=u_400_mode,
            omega_800_mode=omega_800_mode,
            unvalued_letters=unvalued_letters,
            titlo=titlo,
        )
    )


def test_letter_value_anchors() -> None:
    assert _total("а") == 1
    assert _total("ѳ") == 9
    assert _total("і") == 10
    assert _total("ѯ") == 60
    assert _total("р") == 100
    assert _total("ѡ") == 800
    assert _total("ц") == 900


def test_extra_letters_and_u_400_variants() -> None:
    assert _total("ѕ") == 6
    assert _total("ѵ", u_400_mode=U400Mode.IZHITSA) == 400
    assert _total("уѵꙋ", u_400_mode=U400Mode.BOTH) == 1200


def test_koppa_and_cherv_variant() -> None:
    assert _total("ч") == 90
    assert _total("чҁ", koppa_mode=KoppaMode.KOPPA_90, xi_mode=XiMode.CHERV_60) == 150


def test_titlo_can_be_required() -> None:
    assert _total(f"а{cyrillic_slavonic_numerals.TITLO}", titlo=TitloMode.REQUIRED) == 1
    with pytest.raises(ValidationError):
        cyrillic_slavonic_numerals.values("а", titlo=TitloMode.REQUIRED)


@pytest.mark.parametrize("name", ["ѣ", "ж", "John", "שלום", "山田"])
def test_rejects_unsupported_letters(name: str) -> None:
    with pytest.raises(ValidationError):
        cyrillic_slavonic_numerals.values(name)


def test_stable_id_and_version() -> None:
    assert cyrillic_slavonic_numerals.ID == "cyrillic_slavonic_numerals.v1"
    assert cyrillic_slavonic_numerals.VERSION == "1"
