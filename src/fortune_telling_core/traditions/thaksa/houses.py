"""Thai Thaksa house (ภูมิ) data and the birth-day to graha mapping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class House:
    """A Thaksa house, filled in fixed order starting from the birth-day ruler."""

    order: int
    slug: str
    name: str
    thai: str
    meaning: str


# Fixed Thaksa house order: the birth-day graha falls in Boriwan, then the
# Thaksa cycle continues through the remaining houses.
HOUSES: tuple[House, ...] = (
    House(0, "boriwan", "Boriwan", "บริวาร", "Retinue: family, subordinates, dependents."),
    House(1, "ayu", "Ayu", "อายุ", "Self: health, vitality, longevity."),
    House(2, "det", "Det", "เดช", "Power: authority, status, reputation."),
    House(3, "si", "Si", "ศรี", "Fortune: wealth, charm, prosperity."),
    House(4, "mula", "Mula", "มูละ", "Foundation: property, assets, inheritance."),
    House(5, "utsaha", "Utsaha", "อุตสาหะ", "Diligence: effort, work, perseverance."),
    House(6, "montri", "Montri", "มนตรี", "Support: mentors, patrons, counsel."),
    House(7, "kalakini", "Kalakini", "กาลกิณี", "Misfortune: obstacles, adversity, ill omen."),
)

# Proleptic Gregorian weekday (Monday=0 .. Sunday=6) -> Thaksa cycle index of
# the ruling graha. Wednesday maps to Mercury during the day; an evening birth
# is handled separately as the night graha Rahu.
_WEEKDAY_TO_GRAHA: dict[int, int] = {
    6: 0,  # Sunday -> Sun
    0: 1,  # Monday -> Moon
    1: 2,  # Tuesday -> Mars
    2: 3,  # Wednesday (day) -> Mercury
    5: 4,  # Saturday -> Saturn
    3: 5,  # Thursday -> Jupiter
    4: 7,  # Friday -> Venus
}

# Local-clock hour at or after which a Wednesday birth rules under Rahu
# (พุธกลางคืน, Wednesday night) rather than Mercury.
_WEDNESDAY_NIGHT_HOUR = 18

_RAHU_INDEX = 6
_WEDNESDAY = 2


def ruling_graha_index(weekday: int, hour: int) -> int:
    """Return the Thaksa cycle index of the ruling graha for a birth moment.

    Args:
        weekday: Proleptic Gregorian weekday, Monday=0 through Sunday=6.
        hour: Local-clock hour of birth, 0-23. Only consulted for Wednesday,
            where an 18:00-or-later birth rules under Rahu (Wednesday night).

    Returns:
        The ruling graha's Thaksa cycle index.
    """

    if weekday == _WEDNESDAY and hour >= _WEDNESDAY_NIGHT_HOUR:
        return _RAHU_INDEX
    return _WEEKDAY_TO_GRAHA[weekday]
