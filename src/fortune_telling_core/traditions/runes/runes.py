"""Elder Futhark rune data.

The twenty-four runes of the Elder Futhark in their traditional order, grouped
into three ættir (Freyr's, Heimdall's, and Tyr's). Eight runes are symmetrical
under a 180° turn and therefore have no reversed (merkstave) reading; the
``reversible`` flag records this so casting can never reverse them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Rune:
    """One Elder Futhark rune."""

    index: int
    slug: str
    name: str
    glyph: str
    letter: str
    aett: str
    keyword: str
    reversible: bool

    @property
    def symbol_id(self) -> str:
        return f"runes.rune.{self.slug}"


_FREYR = "Freyr"
_HEIMDALL = "Heimdall"
_TYR = "Tyr"

RUNES: tuple[Rune, ...] = (
    Rune(0, "fehu", "Fehu", "ᚠ", "f", _FREYR, "Wealth", True),
    Rune(1, "uruz", "Uruz", "ᚢ", "u", _FREYR, "Strength", True),
    Rune(2, "thurisaz", "Thurisaz", "ᚦ", "th", _FREYR, "Thorn", True),
    Rune(3, "ansuz", "Ansuz", "ᚨ", "a", _FREYR, "Message", True),
    Rune(4, "raidho", "Raidho", "ᚱ", "r", _FREYR, "Journey", True),
    Rune(5, "kenaz", "Kenaz", "ᚲ", "k", _FREYR, "Torch", True),
    Rune(6, "gebo", "Gebo", "ᚷ", "g", _FREYR, "Gift", False),
    Rune(7, "wunjo", "Wunjo", "ᚹ", "w", _FREYR, "Joy", True),
    Rune(8, "hagalaz", "Hagalaz", "ᚺ", "h", _HEIMDALL, "Hail", False),
    Rune(9, "nauthiz", "Nauthiz", "ᚾ", "n", _HEIMDALL, "Need", True),
    Rune(10, "isa", "Isa", "ᛁ", "i", _HEIMDALL, "Ice", False),
    Rune(11, "jera", "Jera", "ᛃ", "j", _HEIMDALL, "Harvest", False),
    Rune(12, "eihwaz", "Eihwaz", "ᛇ", "ei", _HEIMDALL, "Endurance", False),
    Rune(13, "perthro", "Perthro", "ᛈ", "p", _HEIMDALL, "Fate", True),
    Rune(14, "algiz", "Algiz", "ᛉ", "z", _HEIMDALL, "Protection", True),
    Rune(15, "sowilo", "Sowilo", "ᛋ", "s", _HEIMDALL, "Sun", False),
    Rune(16, "tiwaz", "Tiwaz", "ᛏ", "t", _TYR, "Victory", True),
    Rune(17, "berkano", "Berkano", "ᛒ", "b", _TYR, "Growth", True),
    Rune(18, "ehwaz", "Ehwaz", "ᛖ", "e", _TYR, "Movement", True),
    Rune(19, "mannaz", "Mannaz", "ᛗ", "m", _TYR, "Humanity", True),
    Rune(20, "laguz", "Laguz", "ᛚ", "l", _TYR, "Water", True),
    Rune(21, "ingwaz", "Ingwaz", "ᛜ", "ng", _TYR, "Fertility", False),
    Rune(22, "dagaz", "Dagaz", "ᛞ", "d", _TYR, "Breakthrough", False),
    Rune(23, "othala", "Othala", "ᛟ", "o", _TYR, "Heritage", True),
)

RUNE_BY_SLUG = {rune.slug: rune for rune in RUNES}
