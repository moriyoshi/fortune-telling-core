"""Koyomi day-quality spread.

The koyomi engine evaluates the auspiciousness annotations (暦注) of a single
civil day. The headline 六曜 is the selected symbol; the day's 干支, sectional
month, lunisolar date, and the 選日 flags (一粒万倍日 / 三隣亡 / 天赦日) are
recorded as modifiers on that selection.
"""

from fortune_telling_core.spread import Position, Spread

KOYOMI_SPREAD = Spread(
    id="koyomi.spread.day.v1",
    name="Koyomi Day Quality",
    positions=(Position("rokuyo", "Rokuyō", "The day's 六曜, with 干支 and 選日 annotations."),),
)
