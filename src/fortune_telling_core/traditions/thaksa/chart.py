"""Thaksa chart computation and chart-to-draw conversion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.traditions.thaksa.deck import THAKSA_DECK
from fortune_telling_core.traditions.thaksa.grahas import Graha, graha
from fortune_telling_core.traditions.thaksa.houses import HOUSES, ruling_graha_index
from fortune_telling_core.traditions.thaksa.spreads import THAKSA_SPREAD

_RAHU_INDEX = 6
_WED = 2


@dataclass(frozen=True, slots=True)
class ThaksaChart:
    """A resolved Thaksa chart: the eight houses each filled by a graha."""

    ruler: Graha
    """The birth-day ruling graha, seated in the Boriwan house."""

    night: bool
    """Whether the ruler is the Wednesday-night graha (Rahu)."""

    @property
    def placements(self) -> tuple[Graha, ...]:
        """Grahas seated in house order, starting from the ruler in Boriwan."""

        return tuple(graha(self.ruler.index + house.order) for house in HOUSES)

    @property
    def kalakini(self) -> Graha:
        """The graha in the inauspicious Kalakini house."""

        return self.placements[-1]


def compute_chart(birth: datetime) -> ThaksaChart:
    """Compute the Thaksa chart for a birth moment.

    Args:
        birth: Timezone-aware birth datetime. Its wall-clock weekday and hour
            are interpreted in the supplied offset; a Wednesday birth at or
            after 18:00 rules under Rahu (Wednesday night).

    Returns:
        The resolved Thaksa chart.
    """

    index = ruling_graha_index(birth.weekday(), birth.hour)
    ruler = graha(index)
    return ThaksaChart(ruler=ruler, night=ruler.index == _RAHU_INDEX and birth.weekday() == _WED)


def draw_from_chart(chart: ThaksaChart) -> Draw:
    common = {
        "ruler": chart.ruler.name,
        "ruler_thai": chart.ruler.thai,
        "ruler_color": chart.ruler.color,
        "buddha_posture": chart.ruler.buddha_posture,
        "strength": str(chart.ruler.strength),
        "kalakini": chart.kalakini.name,
        "wednesday_night": "true" if chart.night else "false",
    }
    selections = tuple(
        Selection(
            house.slug,
            placed.symbol_id,
            {
                **common,
                "house": house.slug,
                "graha": placed.name,
                "graha_thai": placed.thai,
                "color": placed.color,
                "graha_strength": str(placed.strength),
            },
        )
        for house, placed in zip(HOUSES, chart.placements, strict=True)
    )
    return Draw(THAKSA_DECK.id, THAKSA_SPREAD.id, selections)
