"""Hebrew gematria deck: a single structural result symbol.

Gematria totals are unbounded, so they are not enumerated as deck symbols. The
deck holds one generic result symbol and the actual total is carried in
``Selection.modifiers["total"]`` / ``["value"]``. See the design note
``.agents/docs/design/non-ascii-name-numerology.md``.
"""

from fortune_telling_core.symbols import Deck, Symbol

HEBREW_GEMATRIA_RESULT_SYMBOL = "hebrew_gematria.result.total"

HEBREW_GEMATRIA_DECK = Deck(
    id="hebrew_gematria.deck.total.v1",
    symbols=(
        Symbol(
            id=HEBREW_GEMATRIA_RESULT_SYMBOL,
            name="Gematria Total",
            attributes={"kind": "raw_total"},
        ),
    ),
)
