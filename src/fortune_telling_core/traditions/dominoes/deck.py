"""Domino deck: the 28 tiles of a double-six set."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.dominoes.tiles import TILES

DOMINOES_DECK = Deck(
    id="dominoes.deck.double-six.v1",
    symbols=tuple(
        Symbol(
            id=tile.symbol_id,
            name=tile.name,
            attributes={
                "high": str(tile.high),
                "low": str(tile.low),
                "pips": str(tile.pips),
                "double": "true" if tile.double else "false",
            },
        )
        for tile in TILES
    ),
)
