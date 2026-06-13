"""Modern Cyrillic Pythagorean deck: root numbers 1-9."""

from fortune_telling_core.symbols import Deck, Symbol

CYRILLIC_PYTHAGOREAN_DECK = Deck(
    id="cyrillic_pythagorean.deck.numbers.v1",
    symbols=tuple(
        Symbol(
            id=f"cyrillic_pythagorean.number.{value}",
            name=str(value),
            attributes={"value": str(value), "kind": "root"},
        )
        for value in range(1, 10)
    ),
)
