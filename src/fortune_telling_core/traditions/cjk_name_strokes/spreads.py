"""CJK name stroke onomancy spread."""

from fortune_telling_core.spread import Position, Spread

CJK_NAME_STROKES_SPREAD = Spread(
    id="cjk_name_strokes.spread.five_grid.v1",
    name="CJK Name Stroke Five-Grid",
    positions=(
        Position("heaven", "Heaven", "Surname stroke grid value."),
        Position("person", "Person", "Last surname plus first given-name grid value."),
        Position("earth", "Earth", "Given-name stroke grid value."),
        Position("outer", "Outer", "Total less person grid value."),
        Position("total", "Total", "Total stroke grid value."),
    ),
)
