from datetime import UTC, datetime

from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.traditions.astrology import (
    NATAL_CHART,
    SIDEREAL_ZODIAC,
    TROPICAL_ZODIAC,
    BuiltinEphemeris,
    build_engine,
)
from fortune_telling_core.traditions.astrology.bodies import Body
from fortune_telling_core.traditions.astrology.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.traditions.astrology.positions import EclipticPosition


def test_sidereal_uses_same_sign_symbols_with_different_deck_id() -> None:
    request = ReadingRequest(
        spread_id=NATAL_CHART.id,
        deck_id=SIDEREAL_ZODIAC.id,
        querent=Querent(
            id="native",
            display_name="Native",
            attributes={
                "birth_datetime": datetime(2000, 1, 1, 12, tzinfo=UTC).isoformat(),
                "latitude": "0",
                "longitude": "0",
                "zodiac": "sidereal",
                "ayanamsa": "lahiri",
            },
        ),
    )
    reading = build_engine(
        FixedEphemeris({body: EclipticPosition(25.0, 1.0) for body in Body})
    ).cast(request)

    assert reading.draw.deck_id == SIDEREAL_ZODIAC.id
    assert {symbol.id for symbol in TROPICAL_ZODIAC.symbols} == {
        symbol.id for symbol in SIDEREAL_ZODIAC.symbols
    }


def test_core_imports_do_not_include_astrology() -> None:
    import fortune_telling_core

    assert "astrology" not in fortune_telling_core.__all__


def test_builtin_ephemeris_cast_smoke() -> None:
    request = ReadingRequest(
        spread_id=NATAL_CHART.id,
        deck_id=TROPICAL_ZODIAC.id,
        options={
            "birth_datetime": datetime(2020, 6, 1, 0, tzinfo=UTC).isoformat(),
            "latitude": "35.0",
            "longitude": "139.0",
            "house_system": "equal",
        },
    )
    reading = build_engine(BuiltinEphemeris()).cast(request)

    assert len(reading.draw.selections) == 14
    assert reading.summary is not None
