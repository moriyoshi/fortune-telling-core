"""Modern Cyrillic Pythagorean letter-value system."""

from __future__ import annotations

from enum import StrEnum

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import NameValueUnit, is_ignorable

ID = "cyrillic_pythagorean.v1"
VERSION = "1"


class Language(StrEnum):
    """Supported Cyrillic alphabets."""

    RUSSIAN = "russian"
    UKRAINIAN = "ukrainian"
    SERBIAN = "serbian"
    BULGARIAN = "bulgarian"


class Alphabet(StrEnum):
    """Explicit alphabet tables."""

    RUSSIAN_33 = "russian_33"
    RUSSIAN_32_NO_YO = "russian_32_no_yo"
    UKRAINIAN_33 = "ukrainian_33"
    SERBIAN_30 = "serbian_30"
    BULGARIAN_30 = "bulgarian_30"


class YoMode(StrEnum):
    """How Russian yo is handled."""

    DISTINCT = "distinct"
    FOLD_TO_E = "fold_to_e"


class SignsMode(StrEnum):
    """How hard and soft signs are handled."""

    COUNT = "count"
    IGNORE_HARD_SOFT_SIGNS = "ignore_hard_soft_signs"


class ShortIMode(StrEnum):
    """How short i is handled."""

    DISTINCT = "distinct"
    FOLD_TO_I = "fold_to_i"


class NormalizationMode(StrEnum):
    """Supported normalization modes."""

    STRICT_CYRILLIC = "strict_cyrillic"


_ALPHABETS = {
    Alphabet.RUSSIAN_33: "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    Alphabet.RUSSIAN_32_NO_YO: "абвгдежзийклмнопрстуфхцчшщъыьэюя",
    Alphabet.UKRAINIAN_33: "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя",
    Alphabet.SERBIAN_30: "абвгдђежзијклљмнњопрстћуфхцчџш",
    Alphabet.BULGARIAN_30: "абвгдежзийклмнопрстуфхцчшщъьюя",
}

_DEFAULT_ALPHABET = {
    Language.RUSSIAN: Alphabet.RUSSIAN_33,
    Language.UKRAINIAN: Alphabet.UKRAINIAN_33,
    Language.SERBIAN: Alphabet.SERBIAN_30,
    Language.BULGARIAN: Alphabet.BULGARIAN_30,
}

_ALPHABET_LANGUAGE = {
    Alphabet.RUSSIAN_33: Language.RUSSIAN,
    Alphabet.RUSSIAN_32_NO_YO: Language.RUSSIAN,
    Alphabet.UKRAINIAN_33: Language.UKRAINIAN,
    Alphabet.SERBIAN_30: Language.SERBIAN,
    Alphabet.BULGARIAN_30: Language.BULGARIAN,
}


def values(
    name: str,
    *,
    language: Language = Language.RUSSIAN,
    alphabet: Alphabet | None = None,
    yo_mode: YoMode = YoMode.DISTINCT,
    signs_mode: SignsMode = SignsMode.COUNT,
    short_i_mode: ShortIMode = ShortIMode.DISTINCT,
    normalization: NormalizationMode = NormalizationMode.STRICT_CYRILLIC,
) -> tuple[NameValueUnit, ...]:
    """Return per-letter Cyrillic Pythagorean values for ``name``."""

    if normalization is not NormalizationMode.STRICT_CYRILLIC:
        raise ValidationError(f"unsupported Cyrillic normalization: {normalization!r}")
    resolved_alphabet = alphabet or _DEFAULT_ALPHABET[language]
    if _ALPHABET_LANGUAGE[resolved_alphabet] is not language:
        raise ValidationError(
            f"alphabet {resolved_alphabet.value!r} is not valid for language {language.value!r}"
        )

    letters = _ALPHABETS[resolved_alphabet]
    table = {letter: index % 9 + 1 for index, letter in enumerate(letters)}

    units: list[NameValueUnit] = []
    for original in name.lower():
        char = _normalize_char(
            original,
            alphabet=resolved_alphabet,
            yo_mode=yo_mode,
            signs_mode=signs_mode,
            short_i_mode=short_i_mode,
        )
        if char is None:
            continue
        value = table.get(char)
        if value is not None:
            units.append(NameValueUnit(char, value))
        elif is_ignorable(char):
            continue
        else:
            raise ValidationError(
                "unsupported character for Cyrillic Pythagorean numerology: "
                f"{original!r} (U+{ord(original):04X})"
            )
    return tuple(units)


def _normalize_char(
    char: str,
    *,
    alphabet: Alphabet,
    yo_mode: YoMode,
    signs_mode: SignsMode,
    short_i_mode: ShortIMode,
) -> str | None:
    if char == "ё":
        if alphabet is Alphabet.RUSSIAN_33 and yo_mode is YoMode.DISTINCT:
            return char
        if yo_mode is YoMode.FOLD_TO_E:
            return "е"
    if char in {"ъ", "ь"} and signs_mode is SignsMode.IGNORE_HARD_SOFT_SIGNS:
        return None
    if char == "й" and short_i_mode is ShortIMode.FOLD_TO_I:
        return "и"
    return char


def total(units: tuple[NameValueUnit, ...]) -> int:
    """Return the sum of the values in ``units``."""

    return sum(unit.value for unit in units)


def reduce_to_root(value: int) -> int:
    """Reduce ``value`` to a root from 1 to 9."""

    while value > 9:
        value = sum(int(digit) for digit in str(value))
    return value
