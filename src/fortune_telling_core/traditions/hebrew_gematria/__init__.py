from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Hebrew gematria tradition implementation.

The package exposes a single structural result deck, a one-position total
spread, and an engine builder that deterministically sums the standard gematria
values of a Hebrew name. Gematria compares raw totals, so the total is stamped
in ``Selection.modifiers`` rather than enumerated as deck symbols. Whether the
five final forms take their base value or the mispar gadol values 500-900 is
configurable via ``final_letter_mode``.

Example:
    ```python
    from fortune_telling_core import Querent, ReadingRequest
    from fortune_telling_core.traditions.hebrew_gematria import (
        HEBREW_GEMATRIA_DECK,
        HEBREW_GEMATRIA_SPREAD,
        build_engine,
    )

    request = ReadingRequest(
        deck_id=HEBREW_GEMATRIA_DECK.id,
        spread_id=HEBREW_GEMATRIA_SPREAD.id,
        querent=Querent(id="s", display_name="Sample", attributes={"name": "חיים"}),
    )
    reading = build_engine().cast(request)
    # reading.summary -> "Gematria total 68."
    ```
"""

from fortune_telling_core.traditions._name_values.hebrew_gematria import (  # noqa: E402
    FinalLetterMode,
)
from fortune_telling_core.traditions.hebrew_gematria.deck import (  # noqa: E402
    HEBREW_GEMATRIA_DECK,
)
from fortune_telling_core.traditions.hebrew_gematria.engine import (  # noqa: E402
    HebrewGematriaEngine,
    build_engine,
)
from fortune_telling_core.traditions.hebrew_gematria.spreads import (  # noqa: E402
    HEBREW_GEMATRIA_SPREAD,
)

__all__ = [
    "HEBREW_GEMATRIA_DECK",
    "HEBREW_GEMATRIA_SPREAD",
    "FinalLetterMode",
    "HebrewGematriaEngine",
    "build_engine",
]
