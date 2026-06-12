"""Nine Star Ki spread."""

from fortune_telling_core.spread import Position, Spread

NINE_STAR_KI_SPREAD = Spread(
    id="nsk.spread.natal.v1",
    name="Nine Star Ki",
    positions=(
        Position("principal", "Principal Star", "Year star from the Risshun solar year."),
        Position("monthly", "Monthly Star", "Month star from the sectional solar month."),
        Position("daily", "Daily Star", "Day star from the solstice escapement cycle."),
        Position("tendency", "Tendency Star", "Inclination star from the natal year chart."),
    ),
)
