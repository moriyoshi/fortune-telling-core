"""CJK name stroke onomancy deck: structural five-grid symbols."""

from fortune_telling_core.symbols import Deck, Symbol

GRID_SYMBOLS = {
    "heaven": "cjk_name_strokes.result.heaven",
    "person": "cjk_name_strokes.result.person",
    "earth": "cjk_name_strokes.result.earth",
    "outer": "cjk_name_strokes.result.outer",
    "total": "cjk_name_strokes.result.total",
}

CJK_NAME_STROKES_DECK = Deck(
    id="cjk_name_strokes.deck.five_grid.v1",
    symbols=tuple(
        Symbol(
            id=symbol_id,
            name=f"{position.title()} Grid",
            attributes={"kind": "stroke_grid", "grid_position": position},
        )
        for position, symbol_id in GRID_SYMBOLS.items()
    ),
)
