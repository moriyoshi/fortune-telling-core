"""Heavenly stems, earthly branches, and hidden stems."""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.config import Element, Polarity


@dataclass(frozen=True, slots=True)
class Stem:
    index: int
    slug: str
    cjk: str
    element: Element
    polarity: Polarity


@dataclass(frozen=True, slots=True)
class Branch:
    index: int
    slug: str
    cjk: str
    element: Element
    polarity: Polarity
    animal: str
    hidden_stems: tuple[int, ...]


_ELEMENTS = (Element.WOOD, Element.FIRE, Element.EARTH, Element.METAL, Element.WATER)
_STEM_SLUGS = ("jia", "yi", "bing", "ding", "wu", "ji", "geng", "xin", "ren", "gui")
_STEM_CJK = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")

STEMS: tuple[Stem, ...] = tuple(
    Stem(
        index=index,
        slug=_STEM_SLUGS[index],
        cjk=_STEM_CJK[index],
        element=_ELEMENTS[index // 2],
        polarity=Polarity.YANG if index % 2 == 0 else Polarity.YIN,
    )
    for index in range(10)
)

BRANCHES: tuple[Branch, ...] = (
    Branch(0, "zi", "子", Element.WATER, Polarity.YANG, "Rat", (9,)),
    Branch(1, "chou", "丑", Element.EARTH, Polarity.YIN, "Ox", (5, 9, 7)),
    Branch(2, "yin", "寅", Element.WOOD, Polarity.YANG, "Tiger", (0, 2, 4)),
    Branch(3, "mao", "卯", Element.WOOD, Polarity.YIN, "Rabbit", (1,)),
    Branch(4, "chen", "辰", Element.EARTH, Polarity.YANG, "Dragon", (4, 1, 9)),
    Branch(5, "si", "巳", Element.FIRE, Polarity.YIN, "Snake", (2, 4, 6)),
    Branch(6, "wu", "午", Element.FIRE, Polarity.YANG, "Horse", (3, 5)),
    Branch(7, "wei", "未", Element.EARTH, Polarity.YIN, "Goat", (5, 3, 1)),
    Branch(8, "shen", "申", Element.METAL, Polarity.YANG, "Monkey", (6, 8, 4)),
    Branch(9, "you", "酉", Element.METAL, Polarity.YIN, "Rooster", (7,)),
    Branch(10, "xu", "戌", Element.EARTH, Polarity.YANG, "Dog", (4, 7, 3)),
    Branch(11, "hai", "亥", Element.WATER, Polarity.YIN, "Pig", (8, 0)),
)


def stem(index: int) -> Stem:
    return STEMS[index % 10]


def branch(index: int) -> Branch:
    return BRANCHES[index % 12]


def stem_symbol_id(index: int) -> str:
    return f"fp.stem.{stem(index).slug}"


def branch_symbol_id(index: int) -> str:
    return f"fp.branch.{branch(index).slug}"
