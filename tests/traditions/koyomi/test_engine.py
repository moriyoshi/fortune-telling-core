from datetime import UTC, datetime, timedelta, timezone

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.koyomi import (
    KOYOMI_DECK,
    KOYOMI_SPREAD,
    build_engine,
)


def _modifiers(target: str) -> dict[str, str]:
    reading = build_engine().cast(_request({"target_datetime": target}))
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None
    return dict(modifiers)


def test_deck_has_six_rokuyo() -> None:
    assert len(KOYOMI_DECK.symbols) == 6


def test_rokuyo_anchor_lunar_new_year_is_sensho() -> None:
    # 旧暦 1/1 is 先勝 by definition of the rokuyō cycle.
    modifiers = _modifiers("2024-02-10T12:00:00+09:00")
    assert modifiers["lunisolar"] == "2024-1-1"
    assert modifiers["rokuyo_cjk"] == "先勝"


def test_strongest_lucky_day_2024_01_01() -> None:
    # 2024-01-01 is a 甲子 day in winter: both 天赦日 and 一粒万倍日.
    modifiers = _modifiers("2024-01-01T12:00:00+09:00")
    assert modifiers["day_ganzhi"] == "甲子"
    assert modifiers["tensha"] == "true"
    assert modifiers["ichiryu_manbai"] == "true"
    assert modifiers["rokuyo_cjk"] == "赤口"


def test_spring_tensha_day_2024_03_15() -> None:
    # 2024-03-15 is a 戊寅 day in spring: 天赦日 and 一粒万倍日.
    modifiers = _modifiers("2024-03-15T12:00:00+09:00")
    assert modifiers["day_ganzhi"] == "戊寅"
    assert modifiers["tensha"] == "true"
    assert modifiers["ichiryu_manbai"] == "true"


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request({"target_datetime": "2024-01-01T12:00:00+09:00"})
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert reading.provenance.rng_seed is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "rokuyo=(lunar_month+lunar_day)%6" in reading.provenance.notes


def test_birth_datetime_is_accepted_as_alias() -> None:
    reading = build_engine().cast(_request({"birth_datetime": "2024-01-01T12:00:00+09:00"}))
    assert reading.draw.selections[0].symbol_id == "koyomi.rokuyo.shakko"


def test_as_of_is_used_when_no_explicit_target() -> None:
    request = ReadingRequest(
        spread_id=KOYOMI_SPREAD.id,
        deck_id=KOYOMI_DECK.id,
        as_of=datetime(2024, 1, 1, 12, 0, tzinfo=timezone(timedelta(hours=9))),
    )
    reading = build_engine().cast(request)
    modifiers = reading.draw.selections[0].modifiers
    assert modifiers is not None
    # Same 甲子 day as the explicit-target test above.
    assert modifiers["day_ganzhi"] == "甲子"


def test_target_datetime_overrides_as_of() -> None:
    request = ReadingRequest(
        spread_id=KOYOMI_SPREAD.id,
        deck_id=KOYOMI_DECK.id,
        querent=Querent("subject", "Subject", {"target_datetime": "2024-03-15T12:00:00+09:00"}),
        as_of=datetime(2024, 1, 1, 12, 0, tzinfo=timezone(timedelta(hours=9))),
    )
    modifiers = build_engine().cast(request).draw.selections[0].modifiers
    assert modifiers is not None
    assert modifiers["day_ganzhi"] == "戊寅"


def test_validation_error_on_missing_date() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=KOYOMI_SPREAD.id, deck_id=KOYOMI_DECK.id))


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=KOYOMI_SPREAD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=KOYOMI_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "koyomi" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str]) -> ReadingRequest:
    return ReadingRequest(
        spread_id=KOYOMI_SPREAD.id,
        deck_id=KOYOMI_DECK.id,
        querent=Querent("subject", "Subject", attrs),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
    )
