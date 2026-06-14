# Hebrew Gematria

A Hebrew gematria engine that deterministically sums the standard letter values
(mispar hechrachi, 1-400) of a Hebrew name. Niqqud are stripped and unsupported
characters are rejected. Because gematria compares raw totals, the total is
stamped in the selection modifiers over a single structural result symbol;
standard versus *mispar gadol* finals (500-900) is configurable.

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
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "שלום"}),
)
reading = build_engine().cast(request)
# reading.summary -> "Gematria total 376."
```

::: fortune_telling_core.traditions.hebrew_gematria
