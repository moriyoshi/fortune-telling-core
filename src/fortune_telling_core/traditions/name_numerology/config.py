"""Name numerology configuration enums."""

from enum import StrEnum


class YMode(StrEnum):
    """Whether the letter Y counts as a vowel.

    Numerologists disagree on Y: some always treat it as a consonant, others as
    a vowel (and some judge it per name by sound, which is not deterministic).
    This engine exposes the two deterministic conventions and defaults to
    treating Y as a consonant.
    """

    CONSONANT = "consonant"
    VOWEL = "vowel"


__all__ = ["YMode"]
