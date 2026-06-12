"""Weton spread."""

from fortune_telling_core.spread import Position, Spread

WETON_SPREAD = Spread(
    id="weton.spread.birth.v1",
    name="Weton",
    positions=(
        Position("saptawara", "Saptawara", "Day of the seven-day week with its neptu."),
        Position("pancawara", "Pancawara", "Pasaran of the five-day market week with its neptu."),
    ),
)
