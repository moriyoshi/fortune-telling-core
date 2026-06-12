"""The eight trigrams (bagua)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trigram:
    """One of the eight trigrams."""

    slug: str
    name: str
    glyph: str
    lines: tuple[int, int, int]
    """Lines bottom-to-top, 1 for yang and 0 for yin."""


TRIGRAMS: tuple[Trigram, ...] = (
    Trigram("qian", "Heaven", "☰", (1, 1, 1)),
    Trigram("dui", "Lake", "☱", (1, 1, 0)),
    Trigram("li", "Fire", "☲", (1, 0, 1)),
    Trigram("zhen", "Thunder", "☳", (1, 0, 0)),
    Trigram("xun", "Wind", "☴", (0, 1, 1)),
    Trigram("kan", "Water", "☵", (0, 1, 0)),
    Trigram("gen", "Mountain", "☶", (0, 0, 1)),
    Trigram("kun", "Earth", "☷", (0, 0, 0)),
)

TRIGRAM_BY_SLUG = {trigram.slug: trigram for trigram in TRIGRAMS}
