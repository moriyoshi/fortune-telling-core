"""Zi Wei Dou Shu twelve-palace spread."""

from fortune_telling_core.spread import Position, Spread
from fortune_telling_core.traditions.zi_wei.chart import PALACES

_DESCRIPTIONS: dict[str, str] = {
    "ming": "命宮 — Life palace.",
    "siblings": "兄弟宮 — Siblings palace.",
    "spouse": "夫妻宮 — Spouse palace.",
    "children": "子女宮 — Children palace.",
    "wealth": "財帛宮 — Wealth palace.",
    "health": "疾厄宮 — Health palace.",
    "travel": "遷移宮 — Travel palace.",
    "friends": "僕役宮 — Friends palace.",
    "career": "官祿宮 — Career palace.",
    "property": "田宅宮 — Property palace.",
    "fortune": "福德宮 — Fortune palace.",
    "parents": "父母宮 — Parents palace.",
}

ZI_WEI_SPREAD = Spread(
    id="zi_wei.spread.twelve_palaces.v1",
    name="Zi Wei Twelve Palaces",
    positions=tuple(Position(slug, cjk, _DESCRIPTIONS[slug]) for slug, cjk in PALACES),
)
