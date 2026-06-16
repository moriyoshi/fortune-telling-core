from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris
from fortune_telling_core.astronomy.position import EclipticPosition
from fortune_telling_core.traditions.nine_star_ki import (
    NINE_STAR_KI_DECK,
    NINE_STAR_KI_SPREAD,
    build_engine,
)


class RaisingEphemeris:
    id = "raising"
    version = "0"

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        del body, jd_tt
        raise AssertionError("ephemeris must not be used during replay")

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset({Body.SUN})


def test_cast_replay_and_serde_are_ephemeris_free_on_replay() -> None:
    request = _request()
    reading = build_engine(_sun_at(315.0)).cast(request)
    replayed = build_engine(RaisingEphemeris()).replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert reading.summary is not None
    assert "Annual chart 2024" in reading.summary
    assert "Monthly chart" in reading.summary


def test_cast_records_expected_positions_and_modifiers() -> None:
    reading = build_engine(_sun_at(315.0)).cast(_request())

    assert tuple(selection.position_id for selection in reading.draw.selections) == (
        "principal",
        "monthly",
        "daily",
        "tendency",
    )
    principal = reading.draw.selections[0]
    monthly = reading.draw.selections[1]
    assert principal.modifiers is not None
    assert monthly.modifiers is not None
    assert principal.symbol_id == "nsk.star.3"
    assert principal.modifiers["solar_year"] == "2024"
    assert monthly.symbol_id == "nsk.star.5"
    assert monthly.modifiers["center_case"] == "false"


def test_request_target_year_controls_annual_chart() -> None:
    attrs = _attrs() | {"target_year": "2025"}
    reading = build_engine(_sun_at(315.0)).cast(_request(attrs))
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None

    assert modifiers["annual_star"] == "2"
    assert "Annual chart 2025" in (reading.summary or "")


def test_as_of_drives_annual_chart_when_target_year_absent() -> None:
    attrs = {key: value for key, value in _attrs().items() if key != "target_year"}
    request = ReadingRequest(
        spread_id=NINE_STAR_KI_SPREAD.id,
        deck_id=NINE_STAR_KI_DECK.id,
        querent=Querent("native", "Native", attrs),
        requested_at=datetime(2026, 6, 12, tzinfo=UTC),
        as_of=datetime(2025, 1, 1, tzinfo=UTC),
    )
    reading = build_engine(_sun_at(315.0)).cast(request)
    assert "Annual chart 2025" in (reading.summary or "")


def test_target_year_option_overrides_as_of() -> None:
    attrs = _attrs() | {"target_year": "2024"}
    request = ReadingRequest(
        spread_id=NINE_STAR_KI_SPREAD.id,
        deck_id=NINE_STAR_KI_DECK.id,
        querent=Querent("native", "Native", attrs),
        as_of=datetime(2030, 1, 1, tzinfo=UTC),
    )
    reading = build_engine(_sun_at(315.0)).cast(request)
    assert "Annual chart 2024" in (reading.summary or "")


def test_request_day_star_escapement_override_changes_daily_star_and_provenance() -> None:
    attrs = {
        "birth_datetime": "2024-01-10T00:00:00+00:00",
        "latitude": "0",
        "longitude": "0",
        "target_year": "2024",
    }
    default = build_engine(_sun_at(315.0)).cast(_request(attrs))
    alternate = build_engine(_sun_at(315.0)).cast(
        _request(attrs | {"day_star_escapement": "first_jiazi_after_solstice"})
    )
    default_daily = next(
        selection for selection in default.draw.selections if selection.position_id == "daily"
    )
    alternate_daily = next(
        selection for selection in alternate.draw.selections if selection.position_id == "daily"
    )

    assert default_daily.symbol_id == "nsk.star.7"
    assert alternate_daily.symbol_id == "nsk.star.1"
    assert "day_star_escapement=first_jiazi_after_solstice" in alternate.provenance.notes


def test_validation_errors() -> None:
    with pytest.raises(ValidationError):
        build_engine(_sun_at(315.0)).cast(
            ReadingRequest(
                spread_id=NINE_STAR_KI_SPREAD.id,
                deck_id=NINE_STAR_KI_DECK.id,
                options={
                    "birth_datetime": "2024-02-05T00:00:00+00:00",
                    "latitude": "91",
                    "longitude": "0",
                },
            )
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "nine_star_ki" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=NINE_STAR_KI_SPREAD.id,
        deck_id=NINE_STAR_KI_DECK.id,
        querent=Querent("native", "Native", attrs or _attrs()),
        requested_at=datetime(2026, 6, 12, tzinfo=UTC),
    )


def _attrs() -> dict[str, str]:
    return {
        "birth_datetime": "2024-02-05T00:00:00+00:00",
        "latitude": "0",
        "longitude": "0",
        "target_year": "2024",
    }


def _sun_at(longitude: float) -> Ephemeris:
    return FixedEphemeris({Body.SUN: EclipticPosition(longitude, 1.0)})
