from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Celtic tree calendar (Ogham tree zodiac) tradition implementation.

The package exposes the thirteen-sign deck (Ogham letters and their trees), the
single-position birth spread, and an engine builder that deterministically
classifies a birth date into a tree sign by fixed date ranges. The scheme is
Robert Graves' 20th-century reconstruction, not an attested ancient calendar;
Graves' nameless day (23 December) is folded into Ruis (Elder).

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.celtic_tree import (
        CELTIC_TREE_DECK,
        CELTIC_TREE_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=CELTIC_TREE_DECK.id,
        spread_id=CELTIC_TREE_SPREAD.id,
        querent=Querent(
            id="sample",
            display_name="Sample",
            attributes={"birth_datetime": "1990-07-01T00:00:00+00:00"},
        ),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Celtic tree sign Oak (Duir), Jun 10 – Jul 7."
    ```
"""

from fortune_telling_core.traditions.celtic_tree.deck import CELTIC_TREE_DECK  # noqa: E402
from fortune_telling_core.traditions.celtic_tree.engine import (  # noqa: E402
    CelticTreeEngine,
    build_engine,
)
from fortune_telling_core.traditions.celtic_tree.spreads import CELTIC_TREE_SPREAD  # noqa: E402

__all__ = ["CELTIC_TREE_DECK", "CELTIC_TREE_SPREAD", "CelticTreeEngine", "build_engine"]
