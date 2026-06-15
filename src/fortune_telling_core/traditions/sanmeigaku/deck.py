"""Sanmeigaku star deck (10 main stars + 12 subordinate stars)."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.sanmeigaku.stars import (
    MAIN_STARS,
    SUBORDINATE_STARS,
)

SANMEIGAKU_DECK = Deck(
    id="sanmeigaku.deck.stars.v1",
    symbols=tuple(
        Symbol(
            id=f"sanmeigaku.main.{star.slug}",
            name=f"{star.cjk} {star.name}",
            attributes={"kind": "main_star", "cjk": star.cjk},
        )
        for star in MAIN_STARS.values()
    )
    + tuple(
        Symbol(
            id=f"sanmeigaku.subordinate.{star.slug}",
            name=f"{star.cjk} {star.name}",
            attributes={"kind": "subordinate_star", "cjk": star.cjk},
        )
        for star in SUBORDINATE_STARS.values()
    ),
)
