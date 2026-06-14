# Greek Isopsephy

A Greek isopsephy engine that deterministically sums the Milesian/Ionic
alphabetic numeral values of a Greek word (units, tens, hundreds, including the
archaic signs digamma=6, qoppa=90, sampi=900). Diacritics are stripped and final
sigma is normalized to sigma by default; the raw total is stamped over a single
structural result symbol.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.greek_isopsephy import (
    GREEK_ISOPSEPHY_DECK,
    GREEK_ISOPSEPHY_SPREAD,
    build_engine,
)

request = ReadingRequest(
    deck_id=GREEK_ISOPSEPHY_DECK.id,
    spread_id=GREEK_ISOPSEPHY_SPREAD.id,
    querent=Querent(id="sample", display_name="Sample", attributes={"name": "λόγος"}),
)
reading = build_engine().cast(request)
# reading.summary -> "Isopsephy total 373."
```

::: fortune_telling_core.traditions.greek_isopsephy
