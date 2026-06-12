"""Geomancy shield spread."""

from fortune_telling_core.spread import Position, Spread

_ORD = {1: "first", 2: "second", 3: "third", 4: "fourth"}


def _quad(prefix: str, label: str) -> tuple[Position, ...]:
    return tuple(
        Position(f"{prefix}_{i}", f"{label} {i}", f"The {_ORD[i]} {label}.") for i in (1, 2, 3, 4)
    )


SHIELD = Spread(
    id="geomancy.spread.shield.v1",
    name="Shield Chart",
    positions=(
        *_quad("mother", "Mother"),
        *_quad("daughter", "Daughter"),
        *_quad("niece", "Niece"),
        Position("right_witness", "Right Witness", "Witness formed from the first two Nieces."),
        Position("left_witness", "Left Witness", "Witness formed from the last two Nieces."),
        Position("judge", "Judge", "The verdict, formed from the two Witnesses."),
    ),
)
