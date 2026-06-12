from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Pythagorean name numerology tradition implementation.

The package exposes the number deck (single digits plus master numbers, shared
with the birth-date numerology tradition), the core-numbers spread, and an
engine builder that deterministically reduces a name to its Expression, Soul
Urge, and Personality numbers. Whether Y counts as a vowel is configurable.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.name_numerology import (
        NAME_NUMEROLOGY_DECK,
        NAME_NUMEROLOGY_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=NAME_NUMEROLOGY_DECK.id,
        spread_id=NAME_NUMEROLOGY_SPREAD.id,
        querent=Querent(id="s", display_name="Sample", attributes={"name": "John"}),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Expression 2 (Diplomat); Soul Urge 6 (Nurturer); Personality 5 (Freedom)."
    ```
"""

from fortune_telling_core.traditions.name_numerology.config import YMode  # noqa: E402
from fortune_telling_core.traditions.name_numerology.deck import (  # noqa: E402
    NAME_NUMEROLOGY_DECK,
)
from fortune_telling_core.traditions.name_numerology.engine import (  # noqa: E402
    NameNumerologyEngine,
    build_engine,
)
from fortune_telling_core.traditions.name_numerology.spreads import (  # noqa: E402
    NAME_NUMEROLOGY_SPREAD,
)

__all__ = [
    "NAME_NUMEROLOGY_DECK",
    "NAME_NUMEROLOGY_SPREAD",
    "NameNumerologyEngine",
    "YMode",
    "build_engine",
]
