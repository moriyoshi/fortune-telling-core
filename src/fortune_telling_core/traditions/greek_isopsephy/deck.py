"""Greek isopsephy deck: a single structural result symbol."""

from fortune_telling_core.symbols import Deck, Symbol

GREEK_ISOPSEPHY_RESULT_SYMBOL = "greek_isopsephy.result.total"

GREEK_ISOPSEPHY_DECK = Deck(
    id="greek_isopsephy.deck.total.v1",
    symbols=(
        Symbol(
            id=GREEK_ISOPSEPHY_RESULT_SYMBOL,
            name="Isopsephy Total",
            attributes={"kind": "raw_total"},
        ),
    ),
)
