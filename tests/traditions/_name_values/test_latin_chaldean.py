from string import ascii_uppercase

from fortune_telling_core.traditions._name_values import latin_chaldean


def test_all_26_letters_mapped_to_1_through_8() -> None:
    assert set(latin_chaldean.LETTER_VALUES) == set(ascii_uppercase)
    assert set(latin_chaldean.LETTER_VALUES.values()) == {1, 2, 3, 4, 5, 6, 7, 8}


def test_known_name_values() -> None:
    units = latin_chaldean.values("John")
    assert [(unit.char, unit.value) for unit in units] == [
        ("J", 1),
        ("O", 7),
        ("H", 5),
        ("N", 5),
    ]
    assert latin_chaldean.total(units) == 18


def test_values_fold_case_and_ignore_non_letters() -> None:
    assert latin_chaldean.values("J.O.H.N") == latin_chaldean.values("John")


def test_stable_id_and_version() -> None:
    assert latin_chaldean.ID == "latin_chaldean.v1"
    assert latin_chaldean.VERSION == "1"
