"""Koyomi rokuyō deck."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.koyomi.calendar_notes import ROKUYO

KOYOMI_DECK = Deck(
    id="koyomi.deck.rokuyo.v1",
    symbols=tuple(
        Symbol(
            id=f"koyomi.rokuyo.{slug}",
            name=f"{cjk} {romaji}",
            attributes={"cjk": cjk},
        )
        for slug, cjk, romaji in ROKUYO
    ),
)
