"""The 64 hexagrams in King Wen sequence.

Each hexagram is defined by its lower and upper trigram. Its six-bit value
(bottom line as the least significant bit, yang = 1) is derived from those
trigrams, giving a bijection between the King Wen numbers and the 64 binaries —
checked in the tests.
"""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.iching.trigrams import TRIGRAM_BY_SLUG

# Yijing Hexagram Symbols block: U+4DC0 is hexagram 1 in King Wen order.
_HEXAGRAM_GLYPH_BASE = 0x4DC0


@dataclass(frozen=True, slots=True)
class Hexagram:
    """One of the 64 hexagrams."""

    number: int
    pinyin: str
    english: str
    lower: str
    upper: str

    @property
    def slug(self) -> str:
        return f"hex{self.number}"

    @property
    def symbol_id(self) -> str:
        return f"iching.hexagram.{self.number}"

    @property
    def glyph(self) -> str:
        return chr(_HEXAGRAM_GLYPH_BASE + self.number - 1)

    @property
    def lines(self) -> tuple[int, ...]:
        """Six lines bottom-to-top, 1 for yang and 0 for yin."""

        return TRIGRAM_BY_SLUG[self.lower].lines + TRIGRAM_BY_SLUG[self.upper].lines

    @property
    def binary(self) -> int:
        """Six-bit value, bottom line as the least significant bit."""

        return sum(line << index for index, line in enumerate(self.lines))


# (number, pinyin, english, lower trigram, upper trigram), King Wen order.
_DATA: tuple[tuple[int, str, str, str, str], ...] = (
    (1, "Qian", "Force", "qian", "qian"),
    (2, "Kun", "Field", "kun", "kun"),
    (3, "Zhun", "Sprouting", "zhen", "kan"),
    (4, "Meng", "Enveloping", "kan", "gen"),
    (5, "Xu", "Attending", "qian", "kan"),
    (6, "Song", "Conflict", "kan", "qian"),
    (7, "Shi", "Leading", "kan", "kun"),
    (8, "Bi", "Grouping", "kun", "kan"),
    (9, "Xiaoxu", "Small Accumulating", "qian", "xun"),
    (10, "Lv", "Treading", "dui", "qian"),
    (11, "Tai", "Pervading", "qian", "kun"),
    (12, "Pi", "Obstruction", "kun", "qian"),
    (13, "Tongren", "Concording People", "li", "qian"),
    (14, "Dayou", "Great Possessing", "qian", "li"),
    (15, "Qian", "Humbling", "gen", "kun"),
    (16, "Yu", "Providing-For", "kun", "zhen"),
    (17, "Sui", "Following", "zhen", "dui"),
    (18, "Gu", "Correcting", "xun", "gen"),
    (19, "Lin", "Nearing", "dui", "kun"),
    (20, "Guan", "Viewing", "kun", "xun"),
    (21, "Shike", "Gnawing Bite", "zhen", "li"),
    (22, "Bi", "Adorning", "li", "gen"),
    (23, "Bo", "Stripping", "kun", "gen"),
    (24, "Fu", "Returning", "zhen", "kun"),
    (25, "Wuwang", "Without Embroiling", "zhen", "qian"),
    (26, "Daxu", "Great Accumulating", "qian", "gen"),
    (27, "Yi", "Swallowing", "zhen", "gen"),
    (28, "Daguo", "Great Exceeding", "xun", "dui"),
    (29, "Kan", "Gorge", "kan", "kan"),
    (30, "Li", "Radiance", "li", "li"),
    (31, "Xian", "Conjoining", "gen", "dui"),
    (32, "Heng", "Persevering", "xun", "zhen"),
    (33, "Dun", "Retiring", "gen", "qian"),
    (34, "Dazhuang", "Great Invigorating", "qian", "zhen"),
    (35, "Jin", "Prospering", "kun", "li"),
    (36, "Mingyi", "Darkening of the Light", "li", "kun"),
    (37, "Jiaren", "Dwelling People", "li", "xun"),
    (38, "Kui", "Polarising", "dui", "li"),
    (39, "Jian", "Limping", "gen", "kan"),
    (40, "Jie", "Taking-Apart", "kan", "zhen"),
    (41, "Sun", "Diminishing", "dui", "gen"),
    (42, "Yi", "Augmenting", "zhen", "xun"),
    (43, "Guai", "Displacement", "qian", "dui"),
    (44, "Gou", "Coupling", "xun", "qian"),
    (45, "Cui", "Clustering", "kun", "dui"),
    (46, "Sheng", "Ascending", "xun", "kun"),
    (47, "Kun", "Confining", "kan", "dui"),
    (48, "Jing", "Welling", "xun", "kan"),
    (49, "Ge", "Skinning", "li", "dui"),
    (50, "Ding", "Holding", "xun", "li"),
    (51, "Zhen", "Shake", "zhen", "zhen"),
    (52, "Gen", "Bound", "gen", "gen"),
    (53, "Jian", "Infiltrating", "gen", "xun"),
    (54, "Guimei", "Converting the Maiden", "dui", "zhen"),
    (55, "Feng", "Abounding", "li", "zhen"),
    (56, "Lv", "Sojourning", "gen", "li"),
    (57, "Xun", "Ground", "xun", "xun"),
    (58, "Dui", "Open", "dui", "dui"),
    (59, "Huan", "Dispersing", "kan", "xun"),
    (60, "Jie", "Articulating", "dui", "kan"),
    (61, "Zhongfu", "Center Returning", "dui", "xun"),
    (62, "Xiaoguo", "Small Exceeding", "gen", "zhen"),
    (63, "Jiji", "Already Fording", "li", "kan"),
    (64, "Weiji", "Not Yet Fording", "kan", "li"),
)

HEXAGRAMS: tuple[Hexagram, ...] = tuple(Hexagram(*row) for row in _DATA)

HEXAGRAM_BY_NUMBER = {hexagram.number: hexagram for hexagram in HEXAGRAMS}
HEXAGRAM_BY_BINARY = {hexagram.binary: hexagram for hexagram in HEXAGRAMS}


def hexagram_for_binary(binary: int) -> Hexagram:
    """Return the hexagram for a six-bit line pattern."""

    return HEXAGRAM_BY_BINARY[binary]
