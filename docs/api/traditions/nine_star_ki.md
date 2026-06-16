# Nine Star Ki (九星気学)

A Nine Star Ki engine computing the principal, monthly, daily, and tendency stars, plus the annual
and monthly Lo Shu flying-star charts rendered into the summary.

```python
from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.nine_star_ki import (
    DayStarEscapement,
    NINE_STAR_KI_DECK,
    NINE_STAR_KI_SPREAD,
    build_engine,
)

engine = build_engine(
    target_year=2026,
    day_star_escapement=DayStarEscapement.JIAZI_AT_OR_BEFORE_SOLSTICE,
)
request = ReadingRequest(
    deck_id=NINE_STAR_KI_DECK.id,
    spread_id=NINE_STAR_KI_SPREAD.id,
    querent=Querent(
        id="sample",
        display_name="Sample",
        attributes={
            "birth_datetime": "1990-01-01T12:00:00+00:00",
            "latitude": "51.5074",
            "longitude": "-0.1278",
        },
    ),
)

reading = engine.cast(request)
```

## Day-star escapement

Daily stars reverse direction around the winter and summer solstices, but schools differ on the
anchor day used for the first star in the new arc. `build_engine()` accepts
`day_star_escapement`, and requests may override it with the `day_star_escapement` option.

The default is `jiazi_at_or_before_solstice`, which preserves this package's original behavior:
Star 1 or Star 9 is anchored to the Jia-Zi day at or before the active solstice. The alternative
`first_jiazi_after_solstice` follows the Daily Flying Star convention that anchors Star 1 or Star 9
to the first Jia-Zi day after the relevant solstice. The selected value is recorded in
`Reading.provenance.notes`.

## Annual chart year

The annual flying-star chart year is resolved most-specific-first: an explicit `target_year`
attribute wins, then the request-level [`as_of`](../core.md#natal-vs-timed-readings) moment, then the
engine's build-time `target_year`, then `requested_at`.

::: fortune_telling_core.traditions.nine_star_ki
