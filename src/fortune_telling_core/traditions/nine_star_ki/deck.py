"""Nine Star Ki 9-star deck."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.nine_star_ki.stars import STARS

NINE_STAR_KI_DECK = Deck(
    id="nsk.deck.stars.v1",
    symbols=tuple(
        Symbol(
            id=star.symbol_id,
            name=star.cjk,
            attributes={
                "number": str(star.number),
                "slug": star.slug,
                "cjk": star.cjk,
                "color": star.color,
                "element": star.element,
                "trigram": star.trigram,
                "home_palace": star.home_palace,
            },
        )
        for star in STARS
    ),
)
