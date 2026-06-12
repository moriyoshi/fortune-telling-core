from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Pythagorean numerology tradition implementation.

The package exposes the number deck (single digits plus master numbers 11, 22,
33), the birth spread, and an engine builder that deterministically reduces a
querent's birth date to a Life Path and Birthday number. The Life Path
reduction method is configurable because the two common methods diverge on
master numbers.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.numerology import (
        NUMEROLOGY_DECK,
        NUMEROLOGY_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=NUMEROLOGY_DECK.id,
        spread_id=NUMEROLOGY_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1987-08-17T00:00:00+00:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Life Path 5 (Freedom); Birthday 8 (Power)."
    ```
"""

from fortune_telling_core.traditions.numerology.config import ReductionMethod  # noqa: E402
from fortune_telling_core.traditions.numerology.deck import NUMEROLOGY_DECK  # noqa: E402
from fortune_telling_core.traditions.numerology.engine import (  # noqa: E402
    NumerologyEngine,
    build_engine,
)
from fortune_telling_core.traditions.numerology.spreads import NUMEROLOGY_SPREAD  # noqa: E402

__all__ = [
    "NUMEROLOGY_DECK",
    "NUMEROLOGY_SPREAD",
    "NumerologyEngine",
    "ReductionMethod",
    "build_engine",
]
