"""Can Chi spread: the day and hour pillars."""

from fortune_telling_core.spread import Position, Spread

CAN_CHI_SPREAD = Spread(
    id="cc.spread.dayhour.v1",
    name="Can Chi",
    positions=(
        Position("day_can", "Day Can", "Heavenly stem of the day pillar."),
        Position("day_chi", "Day Chi", "Earthly branch of the day pillar."),
        Position("hour_can", "Hour Can", "Heavenly stem of the hour pillar."),
        Position("hour_chi", "Hour Chi", "Earthly branch of the hour pillar."),
    ),
)
