"""Luck pillar helpers."""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.config import LuckDirectionInput, Polarity
from fortune_telling_core.traditions.four_pillars.sexagenary import annual_index, ganzhi
from fortune_telling_core.traditions.four_pillars.stems_branches import stem


@dataclass(frozen=True, slots=True)
class LuckPillar:
    index: int
    start_age: float
    cycle_index: int

    @property
    def cjk(self) -> str:
        return ganzhi(self.cycle_index).cjk


def luck_forward(year_stem_index: int, gender: LuckDirectionInput) -> bool:
    yang_year = stem(year_stem_index).polarity == Polarity.YANG
    return yang_year == (gender == LuckDirectionInput.MALE)


def luck_pillars(
    month_cycle_index: int,
    *,
    forward: bool,
    start_age: float,
    count: int,
) -> tuple[LuckPillar, ...]:
    step = 1 if forward else -1
    return tuple(
        LuckPillar(
            index=number,
            start_age=start_age + number * 10.0,
            cycle_index=(month_cycle_index + step * (number + 1)) % 60,
        )
        for number in range(count)
    )


def annual_pillar_cjk(year: int) -> str:
    return ganzhi(annual_index(year)).cjk
