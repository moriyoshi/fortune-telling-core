"""Greek isopsephy letter-value system.

Assigns Greek letters their Ionic/Milesian alphabetic numeral values: units
1-9, tens 10-90, and hundreds 100-900. The 24-letter alphabet is extended with
obsolete numeric signs digamma/stigma for 6, qoppa for 90, and sampi for 900.

Greek combining marks are stripped by default and final sigma is normalized to
sigma by default. Whitespace and punctuation are ignored. Any other unsupported
character is rejected, per the No-Silent-Loss policy for new value systems.
"""

from __future__ import annotations

from enum import StrEnum

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import (
    NameValueUnit,
    is_ignorable,
    strip_combining_marks,
)

ID = "greek_isopsephy.v1"
VERSION = "1"


class Era(StrEnum):
    """Supported Greek isopsephy tables."""

    CLASSICAL = "classical"


class DiacriticsMode(StrEnum):
    """How Greek diacritics are handled."""

    STRIPPED = "stripped"


class SigmaMode(StrEnum):
    """How final sigma is handled."""

    FINAL_TO_SIGMA = "final_to_sigma"
    DISTINCT = "distinct"


LETTER_VALUES = {
    "α": 1,
    "β": 2,
    "γ": 3,
    "δ": 4,
    "ε": 5,
    "ϝ": 6,
    "ϛ": 6,
    "ς": 200,
    "ζ": 7,
    "η": 8,
    "θ": 9,
    "ι": 10,
    "κ": 20,
    "λ": 30,
    "μ": 40,
    "ν": 50,
    "ξ": 60,
    "ο": 70,
    "π": 80,
    "ϙ": 90,
    "ϟ": 90,
    "ρ": 100,
    "σ": 200,
    "τ": 300,
    "υ": 400,
    "φ": 500,
    "χ": 600,
    "ψ": 700,
    "ω": 800,
    "ϡ": 900,
    "Ϡ": 900,
}


def values(
    name: str,
    *,
    era: Era = Era.CLASSICAL,
    diacritics: DiacriticsMode = DiacriticsMode.STRIPPED,
    sigma_mode: SigmaMode = SigmaMode.FINAL_TO_SIGMA,
) -> tuple[NameValueUnit, ...]:
    """Return the per-letter isopsephy values for ``name``.

    Args:
        name: The Greek name or word to evaluate.
        era: Letter table to use. Only ``CLASSICAL`` is currently supported.
        diacritics: Diacritic handling. Only ``STRIPPED`` is currently supported.
        sigma_mode: Whether final sigma is normalized to sigma.

    Returns:
        One :class:`NameValueUnit` per Greek value-bearing letter, in input
        order.

    Raises:
        ValidationError: If ``name`` contains a character that is neither a
            supported Greek letter nor ignorable whitespace or punctuation.
    """

    if era is not Era.CLASSICAL:
        raise ValidationError(f"unsupported Greek isopsephy era: {era!r}")
    if diacritics is not DiacriticsMode.STRIPPED:
        raise ValidationError(f"unsupported Greek diacritics mode: {diacritics!r}")

    normalized = strip_combining_marks(name).lower()
    units: list[NameValueUnit] = []
    for char in normalized:
        if sigma_mode is SigmaMode.FINAL_TO_SIGMA and char == "ς":
            char = "σ"
        value = LETTER_VALUES.get(char)
        if value is not None:
            units.append(NameValueUnit(char, value))
        elif is_ignorable(char):
            continue
        else:
            raise ValidationError(
                f"unsupported character for Greek isopsephy: {char!r} (U+{ord(char):04X})"
            )
    return tuple(units)


def total(units: tuple[NameValueUnit, ...]) -> int:
    """Return the sum of the values in ``units``."""

    return sum(unit.value for unit in units)
