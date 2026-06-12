"""Thaksa deck: the eight grahas (planets)."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.thaksa.grahas import GRAHAS

THAKSA_DECK = Deck(
    id="thaksa.deck.grahas.v1",
    symbols=tuple(
        Symbol(
            id=graha.symbol_id,
            name=graha.name,
            attributes={
                "slug": graha.slug,
                "thai": graha.thai,
                "cycle_index": str(graha.index),
                "color": graha.color,
                "buddha_posture": graha.buddha_posture,
                "strength": str(graha.strength),
            },
        )
        for graha in GRAHAS
    ),
)
