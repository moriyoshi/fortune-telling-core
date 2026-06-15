from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.zi_wei import (
    ZI_WEI_DECK,
    ZI_WEI_SPREAD,
    build_engine,
)

_BIRTH = "1985-04-29T10:00:00+08:00"


def test_deck_and_spread_shapes() -> None:
    assert len(ZI_WEI_DECK.symbols) == 12
    assert len(ZI_WEI_SPREAD.positions) == 12
    assert ZI_WEI_SPREAD.positions[0].id == "ming"


def test_cast_records_twelve_palaces_in_order() -> None:
    reading = build_engine().cast(_request())

    assert tuple(s.position_id for s in reading.draw.selections) == tuple(
        p.id for p in ZI_WEI_SPREAD.positions
    )
    ming = reading.draw.selections[0]
    assert ming.modifiers is not None
    # 命宮 in 未 holds 天府 for this birth; bureau is 木三局 (3).
    assert ming.modifiers["branch_cjk"] == "未"
    assert ming.modifiers["stars_cjk"] == "天府"
    assert ming.modifiers["bureau"] == "3"
    assert reading.summary is not None
    assert "木三局" in reading.summary


def test_each_palace_has_a_branch_and_all_majors_present() -> None:
    reading = build_engine().cast(_request())
    stars: list[str] = []
    branches: list[str] = []
    for selection in reading.draw.selections:
        assert selection.modifiers is not None
        branches.append(selection.modifiers["branch_cjk"])
        if selection.modifiers["stars_cjk"]:
            stars.extend(selection.modifiers["stars_cjk"].split(","))
    assert len(set(branches)) == 12  # palaces cover all twelve branches
    assert len(stars) == 14  # all major stars placed exactly once


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert reading.provenance.rng_seed is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "stars=14_major" in reading.provenance.notes


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(ReadingRequest(spread_id=ZI_WEI_SPREAD.id, deck_id=ZI_WEI_DECK.id))


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=ZI_WEI_SPREAD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=ZI_WEI_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "zi_wei" not in fortune_telling_core.__all__


def _request() -> ReadingRequest:
    return ReadingRequest(
        spread_id=ZI_WEI_SPREAD.id,
        deck_id=ZI_WEI_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": _BIRTH}),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
    )
