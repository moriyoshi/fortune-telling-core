"""Old Cyrillic numerals deck: a single structural result symbol."""

from fortune_telling_core.symbols import Deck, Symbol

CYRILLIC_SLAVONIC_NUMERALS_RESULT_SYMBOL = "cyrillic_slavonic_numerals.result.total"

CYRILLIC_SLAVONIC_NUMERALS_DECK = Deck(
    id="cyrillic_slavonic_numerals.deck.total.v1",
    symbols=(
        Symbol(
            id=CYRILLIC_SLAVONIC_NUMERALS_RESULT_SYMBOL,
            name="Old Cyrillic Numeral Total",
            attributes={"kind": "raw_total"},
        ),
    ),
)
