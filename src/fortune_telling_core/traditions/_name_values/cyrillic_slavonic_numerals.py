"""Old Cyrillic / Church Slavonic numeral value system."""

from __future__ import annotations

from enum import StrEnum

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import (
    NameValueUnit,
    is_ignorable,
    strip_combining_marks,
)

ID = "cyrillic_slavonic_numerals.v1"
VERSION = "1"

TITLO = "\u0483"


class LetterTable(StrEnum):
    """Supported Old Cyrillic numeral tables."""

    COMMON_CHURCH_SLAVONIC = "common_church_slavonic"


class KoppaMode(StrEnum):
    """How the value 90 is represented."""

    CHERV_90 = "cherv_90"
    KOPPA_90 = "koppa_90"


class XiMode(StrEnum):
    """How the value 60 is represented."""

    KSI_60 = "ksi_60"
    CHERV_60 = "cherv_60"


class U400Mode(StrEnum):
    """Which letter forms are accepted for value 400."""

    UK = "uk"
    IZHITSA = "izhitsa"
    BOTH = "both"


class Omega800Mode(StrEnum):
    """Which letter forms are accepted for value 800."""

    OMEGA = "omega"
    OT = "ot"
    BROAD_OMEGA = "broad_omega"


class UnvaluedLettersMode(StrEnum):
    """How obsolete but unvalued letters are handled."""

    REJECT = "reject"


class TitloMode(StrEnum):
    """Whether a titlo mark is required in the input."""

    OPTIONAL = "optional"
    REQUIRED = "required"


_BASE_VALUES = {
    "а": 1,
    "в": 2,
    "г": 3,
    "д": 4,
    "е": 5,
    "є": 5,
    "ѕ": 6,
    "з": 7,
    "и": 8,
    "ѳ": 9,
    "і": 10,
    "к": 20,
    "л": 30,
    "м": 40,
    "н": 50,
    "о": 70,
    "п": 80,
    "р": 100,
    "с": 200,
    "т": 300,
    "ф": 500,
    "х": 600,
    "ѱ": 700,
    "ц": 900,
}


def values(
    name: str,
    *,
    letter_table: LetterTable = LetterTable.COMMON_CHURCH_SLAVONIC,
    koppa_mode: KoppaMode = KoppaMode.CHERV_90,
    xi_mode: XiMode = XiMode.KSI_60,
    u_400_mode: U400Mode = U400Mode.UK,
    omega_800_mode: Omega800Mode = Omega800Mode.OMEGA,
    unvalued_letters: UnvaluedLettersMode = UnvaluedLettersMode.REJECT,
    titlo: TitloMode = TitloMode.OPTIONAL,
) -> tuple[NameValueUnit, ...]:
    """Return per-letter Old Cyrillic numeral values for ``name``."""

    if letter_table is not LetterTable.COMMON_CHURCH_SLAVONIC:
        raise ValidationError(f"unsupported Old Cyrillic letter_table: {letter_table!r}")
    if unvalued_letters is not UnvaluedLettersMode.REJECT:
        raise ValidationError(f"unsupported unvalued_letters mode: {unvalued_letters!r}")
    if xi_mode is XiMode.CHERV_60 and koppa_mode is KoppaMode.CHERV_90:
        raise ValidationError("xi_mode=cherv_60 requires koppa_mode=koppa_90")
    if titlo is TitloMode.REQUIRED and TITLO not in name:
        raise ValidationError("titlo=required but no titlo mark was found")

    table = _table(koppa_mode=koppa_mode, xi_mode=xi_mode, u_400_mode=u_400_mode)
    table = _with_omega(table, omega_800_mode)

    units: list[NameValueUnit] = []
    for char in strip_combining_marks(name).lower():
        value = table.get(char)
        if value is not None:
            units.append(NameValueUnit(char, value))
        elif is_ignorable(char):
            continue
        else:
            raise ValidationError(
                f"unsupported character for Old Cyrillic numerals: {char!r} (U+{ord(char):04X})"
            )
    return tuple(units)


def _table(
    *,
    koppa_mode: KoppaMode,
    xi_mode: XiMode,
    u_400_mode: U400Mode,
) -> dict[str, int]:
    table = dict(_BASE_VALUES)
    if xi_mode is XiMode.KSI_60:
        table["ѯ"] = 60
    else:
        table["ч"] = 60
    if koppa_mode is KoppaMode.CHERV_90:
        table["ч"] = 90
    else:
        table["ҁ"] = 90

    if u_400_mode is U400Mode.UK:
        table["у"] = 400
        table["ꙋ"] = 400
    elif u_400_mode is U400Mode.IZHITSA:
        table["ѵ"] = 400
    else:
        table["у"] = 400
        table["ꙋ"] = 400
        table["ѵ"] = 400
    return table


def _with_omega(table: dict[str, int], omega_800_mode: Omega800Mode) -> dict[str, int]:
    table = dict(table)
    if omega_800_mode is Omega800Mode.OMEGA:
        table["ѡ"] = 800
    elif omega_800_mode is Omega800Mode.OT:
        table["ѿ"] = 800
    else:
        table["ѻ"] = 800
    return table


def total(units: tuple[NameValueUnit, ...]) -> int:
    """Return the sum of the values in ``units``."""

    return sum(unit.value for unit in units)
