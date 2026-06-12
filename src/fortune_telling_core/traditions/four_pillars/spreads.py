"""Four Pillars spread."""

from fortune_telling_core.spread import Position, Spread

FOUR_PILLARS_SPREAD = Spread(
    id="fp.spread.natal.v1",
    name="Four Pillars",
    positions=(
        Position("year_stem", "Year Stem", "Heavenly stem of the year pillar."),
        Position("year_branch", "Year Branch", "Earthly branch of the year pillar."),
        Position("month_stem", "Month Stem", "Heavenly stem of the month pillar."),
        Position("month_branch", "Month Branch", "Earthly branch of the month pillar."),
        Position("day_stem", "Day Stem", "Heavenly stem of the day pillar and Day Master."),
        Position("day_branch", "Day Branch", "Earthly branch of the day pillar."),
        Position("hour_stem", "Hour Stem", "Heavenly stem of the hour pillar."),
        Position("hour_branch", "Hour Branch", "Earthly branch of the hour pillar."),
    ),
)
