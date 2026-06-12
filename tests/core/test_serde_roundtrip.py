from datetime import UTC, datetime

from fortune_telling_core import (
    SCHEMA_VERSION,
    Draw,
    Position,
    PositionReading,
    Provenance,
    Querent,
    Reading,
    ReadingRequest,
    Selection,
    Spread,
    Symbol,
    reading_from_json,
    reading_to_json,
)


def test_value_objects_round_trip_through_dicts() -> None:
    symbol = Symbol("symbol", "Symbol", {"kind": "test"})
    assert Symbol.from_dict(symbol.to_dict()) == symbol

    spread = Spread("spread", "Spread", (Position("focus", "Focus", "Description"),))
    assert Spread.from_dict(spread.to_dict()) == spread

    draw = Draw("deck", "spread", (Selection("focus", "symbol", {"orientation": "upright"}),))
    assert Draw.from_dict(draw.to_dict()) == draw


def test_reading_json_round_trip() -> None:
    requested_at = datetime(2026, 6, 12, 9, 0, tzinfo=UTC)
    created_at = datetime(2026, 6, 12, 9, 1, tzinfo=UTC)
    request = ReadingRequest(
        spread_id="spread",
        deck_id="deck",
        querent=Querent("q", "Querent"),
        requested_at=requested_at,
    )
    spread = Spread("spread", "Spread", (Position("focus", "Focus"),))
    selection = Selection("focus", "symbol")
    symbol = Symbol("symbol", "Symbol")
    reading = Reading(
        request=request,
        spread=spread,
        draw=Draw("deck", "spread", (selection,)),
        positions=(PositionReading(spread.positions[0], symbol, selection),),
        summary=None,
        provenance=Provenance(
            engine_id="engine",
            engine_version="1",
            library_version="0.1.0",
            deck_id="deck",
            spread_id="spread",
            created_at=created_at,
        ),
        schema_version=SCHEMA_VERSION,
    )

    assert reading_from_json(reading_to_json(reading)) == reading
