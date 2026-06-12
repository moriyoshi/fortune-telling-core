"""Sexagenary cycle helpers."""

from __future__ import annotations

from dataclasses import dataclass

from fortune_telling_core.traditions.four_pillars.stems_branches import branch, stem


@dataclass(frozen=True, slots=True)
class GanZhi:
    index: int
    stem_index: int
    branch_index: int

    @property
    def cjk(self) -> str:
        return f"{stem(self.stem_index).cjk}{branch(self.branch_index).cjk}"

    @property
    def slug(self) -> str:
        return f"{stem(self.stem_index).slug}_{branch(self.branch_index).slug}"


CYCLE: tuple[GanZhi, ...] = tuple(GanZhi(index, index % 10, index % 12) for index in range(60))


def ganzhi(index: int) -> GanZhi:
    return CYCLE[index % 60]


def index_for(stem_index: int, branch_index: int) -> int:
    for item in CYCLE:
        if item.stem_index == stem_index % 10 and item.branch_index == branch_index % 12:
            return item.index
    raise ValueError("invalid stem/branch parity")


def annual_index(year: int) -> int:
    return (year - 1984) % 60
