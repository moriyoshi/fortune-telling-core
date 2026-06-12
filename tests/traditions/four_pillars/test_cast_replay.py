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
from fortune_telling_core.traditions.four_pillars import (
    FOUR_PILLARS_DECK,
    FOUR_PILLARS_SPREAD,
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


def test_cast_replay_and_serde() -> None:
    request = _request()
    reading = build_engine(_sun_at(320.0)).cast(request)
    replayed = build_engine(RaisingEphemeris()).replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert reading.summary is not None
    assert "Luck Pillars" in reading.summary


def test_late_zishi_changes_day_pillar() -> None:
    attrs = _attrs() | {"birth_datetime": "1984-02-02T23:30:00+00:00", "day_boundary": "late_zishi"}
    request = ReadingRequest(
        spread_id=FOUR_PILLARS_SPREAD.id,
        deck_id=FOUR_PILLARS_DECK.id,
        querent=Querent("native", "Native", attrs),
    )
    reading = build_engine(_sun_at(320.0)).cast(request)
    day_stem = next(
        selection for selection in reading.draw.selections if selection.position_id == "day_stem"
    )

    assert day_stem.symbol_id == "fp.stem.yi"


def test_time_model_switch_can_change_hour() -> None:
    attrs = _attrs() | {
        "birth_datetime": "1984-02-02T01:30:00+08:00",
        "longitude": "150",
        "time_model": "lmt",
    }
    request = ReadingRequest(
        spread_id=FOUR_PILLARS_SPREAD.id,
        deck_id=FOUR_PILLARS_DECK.id,
        querent=Querent("native", "Native", attrs),
    )
    reading = build_engine(_sun_at(320.0)).cast(request)
    hour_branch = next(
        selection for selection in reading.draw.selections if selection.position_id == "hour_branch"
    )

    assert hour_branch.symbol_id == "fp.branch.yin"


def test_validation_errors() -> None:
    with pytest.raises(ValidationError):
        build_engine(_sun_at(320.0)).cast(
            ReadingRequest(
                spread_id=FOUR_PILLARS_SPREAD.id,
                deck_id=FOUR_PILLARS_DECK.id,
                options={
                    "birth_datetime": "1984-02-02T00:00:00+00:00",
                    "latitude": "0",
                    "longitude": "0",
                },
            )
        )


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "four_pillars" not in fortune_telling_core.__all__


def _request() -> ReadingRequest:
    return ReadingRequest(
        spread_id=FOUR_PILLARS_SPREAD.id,
        deck_id=FOUR_PILLARS_DECK.id,
        querent=Querent("native", "Native", _attrs()),
    )


def _attrs() -> dict[str, str]:
    return {
        "birth_datetime": "1984-02-02T00:30:00+00:00",
        "latitude": "0",
        "longitude": "0",
        "gender": "male",
        "target_year": "2024",
        "luck_count": "3",
    }


def _sun_at(longitude: float) -> Ephemeris:
    return FixedEphemeris({Body.SUN: EclipticPosition(longitude, 1.0)})
