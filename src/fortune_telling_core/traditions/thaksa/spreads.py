"""Thaksa spread: the eight houses."""

from fortune_telling_core.spread import Position, Spread
from fortune_telling_core.traditions.thaksa.houses import HOUSES

THAKSA_SPREAD = Spread(
    id="thaksa.spread.houses.v1",
    name="Thaksa",
    positions=tuple(Position(house.slug, house.name, house.meaning) for house in HOUSES),
)
