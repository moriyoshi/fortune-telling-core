from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.astrology import (
    NATAL_CHART,
    TROPICAL_ZODIAC,
    FixedEphemeris,
    build_engine,
)
from fortune_telling_core.traditions.astrology.bodies import Body
from fortune_telling_core.traditions.astrology.ephemeris.protocol import Ephemeris
from fortune_telling_core.traditions.astrology.positions import EclipticPosition


class RaisingEphemeris:
    id = "raising"
    version = "0"

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset(Body)

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        del body, jd_tt
        raise AssertionError("ephemeris must not be used during replay")


def test_cast_is_deterministic_and_rng_free() -> None:
    engine = build_engine(_fixed_ephemeris())
    request = _request()

    first = engine.cast(request)
    second = engine.cast(request)

    assert first == second
    assert first.provenance.rng_kind is None
    assert (first.draw.selections[0].modifiers or {})["house"] == "7"
    assert "ephemeris=astro.ephemeris.fixed@0.1.0" in first.provenance.notes


def test_replay_is_self_sufficient_without_ephemeris() -> None:
    request = _request()
    reading = build_engine(_fixed_ephemeris()).cast(request)
    replayed = build_engine(RaisingEphemeris()).replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.positions == reading.positions
    assert replayed.summary == reading.summary


def test_astrology_reading_round_trips_through_core_serde() -> None:
    reading = build_engine(_fixed_ephemeris()).cast(_request())

    assert reading_from_json(reading_to_json(reading)) == reading


def test_malformed_birth_data_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        build_engine(_fixed_ephemeris()).cast(
            ReadingRequest(
                spread_id=NATAL_CHART.id,
                deck_id=TROPICAL_ZODIAC.id,
                options={
                    "birth_datetime": "2020-01-01T00:00:00+00:00",
                    "latitude": "91",
                    "longitude": "0",
                },
            )
        )


def _request() -> ReadingRequest:
    return ReadingRequest(
        spread_id=NATAL_CHART.id,
        deck_id=TROPICAL_ZODIAC.id,
        querent=Querent(
            id="native",
            display_name="Native",
            attributes={
                "birth_datetime": datetime(1990, 1, 1, 12, tzinfo=UTC).isoformat(),
                "latitude": "0",
                "longitude": "0",
                "house_system": "whole_sign",
            },
        ),
    )


def _fixed_ephemeris() -> Ephemeris:
    return FixedEphemeris(
        {
            Body.SUN: EclipticPosition(5.0, 1.0),
            Body.MOON: EclipticPosition(35.0, 13.0),
            Body.MERCURY: EclipticPosition(65.0, -1.0),
            Body.VENUS: EclipticPosition(95.0, 1.0),
            Body.MARS: EclipticPosition(125.0, 1.0),
            Body.JUPITER: EclipticPosition(155.0, 1.0),
            Body.SATURN: EclipticPosition(185.0, 1.0),
            Body.URANUS: EclipticPosition(215.0, 1.0),
            Body.NEPTUNE: EclipticPosition(245.0, 1.0),
            Body.PLUTO: EclipticPosition(275.0, 1.0),
            Body.NORTH_NODE: EclipticPosition(305.0, -0.1),
        }
    )
