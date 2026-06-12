"""I Ching spread."""

from fortune_telling_core.spread import Position, Spread

CASTING = Spread(
    id="iching.spread.casting.v1",
    name="Casting",
    positions=(
        Position("primary", "Primary", "The hexagram cast from the six lines."),
        Position("relating", "Relating", "The hexagram after the changing lines transform."),
    ),
)
