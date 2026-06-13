"""Hebrew gematria spread: a single total position."""

from fortune_telling_core.spread import Position, Spread

HEBREW_GEMATRIA_SPREAD = Spread(
    id="hebrew_gematria.spread.name.v1",
    name="Hebrew Gematria Total",
    positions=(Position("total", "Total", "The summed gematria value of the name."),),
)
