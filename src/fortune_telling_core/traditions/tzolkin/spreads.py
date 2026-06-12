"""Tzolk'in spread."""

from fortune_telling_core.spread import Position, Spread

TZOLKIN_SPREAD = Spread(
    id="tzolkin.spread.birth.v1",
    name="Tzolk'in",
    positions=(Position("day_sign", "Day Sign", "Tzolk'in day sign with its trecena number."),),
)
