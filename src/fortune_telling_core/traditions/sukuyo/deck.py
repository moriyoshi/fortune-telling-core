"""Sukuyō 27-mansion deck."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.sukuyo.mansions import MANSIONS

SUKUYO_DECK = Deck(
    id="sukuyo.deck.mansions27.v1",
    symbols=tuple(
        Symbol(
            id=f"sukuyo.mansion.{mansion.slug}",
            name=f"{mansion.cjk} ({mansion.nakshatra})",
            attributes={
                "cjk": mansion.cjk,
                "nakshatra": mansion.nakshatra,
                "index": str(mansion.index),
            },
        )
        for mansion in MANSIONS
    ),
)
