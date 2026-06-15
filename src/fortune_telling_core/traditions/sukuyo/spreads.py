"""Sukuyō birth-mansion spread."""

from fortune_telling_core.spread import Position, Spread

SUKUYO_SPREAD = Spread(
    id="sukuyo.spread.birth_mansion.v1",
    name="Sukuyō Birth Mansion",
    positions=(
        Position(
            "birth_mansion",
            "Birth Mansion",
            "The 本命宿 — the lunar mansion the Moon occupied at birth.",
        ),
    ),
)
