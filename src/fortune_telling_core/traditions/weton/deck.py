"""Weton deck: the seven saptawara days and five pancawara pasaran."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.weton.calendar import PANCAWARA, SAPTAWARA

WETON_DECK = Deck(
    id="weton.deck.javanese.v1",
    symbols=(
        *(
            Symbol(
                id=day.symbol_id,
                name=day.name,
                attributes={
                    "cycle": "saptawara",
                    "slug": day.slug,
                    "javanese": day.javanese,
                    "weekday": str(day.weekday),
                    "neptu": str(day.neptu),
                },
            )
            for day in SAPTAWARA
        ),
        *(
            Symbol(
                id=pasaran.symbol_id,
                name=pasaran.name,
                attributes={
                    "cycle": "pancawara",
                    "slug": pasaran.slug,
                    "javanese": pasaran.javanese,
                    "index": str(pasaran.index),
                    "neptu": str(pasaran.neptu),
                },
            )
            for pasaran in PANCAWARA
        ),
    ),
)
