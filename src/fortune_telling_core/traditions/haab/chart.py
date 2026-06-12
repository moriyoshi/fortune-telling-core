"""Haab' chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.haab.deck import HAAB_DECK
from fortune_telling_core.traditions.haab.months import HaabDate
from fortune_telling_core.traditions.haab.spreads import HAAB_SPREAD


def draw_from_date(haab: HaabDate) -> Draw:
    selection = Selection(
        "haab",
        haab.month.symbol_id,
        {
            "haab": haab.name,
            "month": haab.month.name,
            "day": str(haab.day),
            "wayeb": "true" if haab.month.slug == "wayeb" else "false",
        },
    )
    return Draw(HAAB_DECK.id, HAAB_SPREAD.id, (selection,))
