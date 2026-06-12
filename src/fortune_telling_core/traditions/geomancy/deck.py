"""Geomancy deck: the sixteen figures."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.geomancy.figures import FIGURES

GEOMANCY_DECK = Deck(
    id="geomancy.deck.figures.v1",
    symbols=tuple(
        Symbol(
            id=figure.symbol_id,
            name=figure.name,
            attributes={
                "slug": figure.slug,
                "english": figure.english,
                "element": figure.ruling_element,
                "rows": "".join(str(row) for row in figure.rows),
                "points": str(figure.points),
            },
        )
        for figure in FIGURES
    ),
)
