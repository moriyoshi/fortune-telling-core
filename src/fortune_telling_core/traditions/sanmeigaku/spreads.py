"""Sanmeigaku 人体星図 spread.

Sanmeigaku reads the year, month, and day pillars (the hour pillar is not
used). The chart yields eight stars: five 主星 (main stars) and three 従星
(subordinate stars).

Positions are named by their *source* — the stem or branch the star is derived
from — rather than by the geographic 人体星図 cell (北/南/東/西/中央 and the
shoulder/foot positions). The spatial arrangement and the 初年/中年/晩年 life-
stage labelling vary between teachers and are a presentation concern for an
interpretation layer; the structural facts recorded here are which star each
source yields.
"""

from fortune_telling_core.spread import Position, Spread

SANMEIGAKU_SPREAD = Spread(
    id="sanmeigaku.spread.jintai.v1",
    name="Sanmeigaku Body Star Chart",
    positions=(
        Position("year_stem", "Year Stem Star", "主星 from the year heavenly stem (年干)."),
        Position("month_stem", "Month Stem Star", "主星 from the month heavenly stem (月干)."),
        Position(
            "year_branch",
            "Year Branch Star",
            "主星 from the year branch principal hidden stem (年支元命).",
        ),
        Position(
            "month_branch",
            "Month Branch Star",
            "主星 from the month branch principal hidden stem (月支元命).",
        ),
        Position(
            "day_branch",
            "Day Branch Star",
            "主星 from the day branch principal hidden stem (日支元命); the chart centre.",
        ),
        Position(
            "year_branch_subordinate",
            "Year Branch Subordinate Star",
            "従星 of the day stem at the year branch (年支).",
        ),
        Position(
            "month_branch_subordinate",
            "Month Branch Subordinate Star",
            "従星 of the day stem at the month branch (月支).",
        ),
        Position(
            "day_branch_subordinate",
            "Day Branch Subordinate Star",
            "従星 of the day stem at the day branch (日支).",
        ),
    ),
)
