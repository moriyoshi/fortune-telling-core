"""Tzolk'in chart-to-draw conversion."""

from __future__ import annotations

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.tzolkin.daysigns import TzolkinDay
from fortune_telling_core.traditions.tzolkin.deck import TZOLKIN_DECK
from fortune_telling_core.traditions.tzolkin.spreads import TZOLKIN_SPREAD


def draw_from_day(day: TzolkinDay) -> Draw:
    selection = Selection(
        "day_sign",
        day.sign.symbol_id,
        {
            "tzolkin": day.name,
            "number": str(day.number),
            "sign": day.sign.name,
            "keyword": day.sign.keyword,
            "direction": day.sign.direction,
        },
    )
    return Draw(TZOLKIN_DECK.id, TZOLKIN_SPREAD.id, (selection,))
