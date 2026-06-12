"""Nine Star Ki star data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NineStar:
    number: int
    slug: str
    cjk: str
    color: str
    element: str
    trigram: str
    home_palace: str

    @property
    def symbol_id(self) -> str:
        return f"nsk.star.{self.number}"


STARS: tuple[NineStar, ...] = (
    NineStar(1, "one-white-water", "一白水星", "white", "water", "kan", "N"),
    NineStar(2, "two-black-earth", "二黒土星", "black", "earth", "kun", "SW"),
    NineStar(3, "three-jade-wood", "三碧木星", "jade", "wood", "zhen", "E"),
    NineStar(4, "four-green-wood", "四緑木星", "green", "wood", "xun", "SE"),
    NineStar(5, "five-yellow-earth", "五黄土星", "yellow", "earth", "center", "C"),
    NineStar(6, "six-white-metal", "六白金星", "white", "metal", "qian", "NW"),
    NineStar(7, "seven-red-metal", "七赤金星", "red", "metal", "dui", "W"),
    NineStar(8, "eight-white-earth", "八白土星", "white", "earth", "gen", "NE"),
    NineStar(9, "nine-purple-fire", "九紫火星", "purple", "fire", "li", "S"),
)

STAR_BY_NUMBER = {star.number: star for star in STARS}
HOME_PALACE = {star.number: star.home_palace for star in STARS}
HOME_STAR_BY_PALACE = {star.home_palace: star.number for star in STARS}


def star(number: int) -> NineStar:
    return STAR_BY_NUMBER[_wrap_star(number)]


def _wrap_star(value: int) -> int:
    return ((value - 1) % 9) + 1
