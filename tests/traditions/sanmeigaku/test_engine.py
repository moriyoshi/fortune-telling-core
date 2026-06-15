from datetime import UTC, datetime

import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.sanmeigaku import (
    SANMEIGAKU_DECK,
    SANMEIGAKU_SPREAD,
    build_engine,
)

# 1984-02-02 is the day-pillar epoch (甲子). At noon JST the year pillar is the
# pre-立春 癸亥 and the month pillar 乙丑, giving a stable reference chart.
_BIRTH = "1984-02-02T12:00:00+09:00"


def test_cast_records_expected_positions_and_stars() -> None:
    reading = build_engine().cast(_request())

    assert tuple(s.position_id for s in reading.draw.selections) == (
        "year_stem",
        "month_stem",
        "year_branch",
        "month_branch",
        "day_branch",
        "year_branch_subordinate",
        "month_branch_subordinate",
        "day_branch_subordinate",
    )
    by_position = {s.position_id: s for s in reading.draw.selections}
    # Day pillar 甲子: centre 主星 from 子 (元命 癸) is 玉堂星.
    assert by_position["day_branch"].symbol_id == "sanmeigaku.main.gyokudo"
    assert by_position["day_branch"].modifiers is not None
    assert by_position["day_branch"].modifiers["day_master"] == "甲"
    # 従星 of 甲 at 子 is 天恍星.
    assert by_position["day_branch_subordinate"].symbol_id == "sanmeigaku.subordinate.tenkou"
    assert reading.summary is not None
    assert "玉堂星" in reading.summary


def test_cast_replay_and_serde_are_deterministic() -> None:
    request = _request()
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert reading.provenance.rng_kind is None
    assert reading.provenance.rng_seed is None
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "pillars=year-month-day" in reading.provenance.notes
    assert "hidden_stem_rule=primary" in reading.provenance.notes


def test_validation_error_on_missing_birth_datetime() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(
            ReadingRequest(spread_id=SANMEIGAKU_SPREAD.id, deck_id=SANMEIGAKU_DECK.id)
        )


def test_unsupported_deck_and_spread() -> None:
    engine = build_engine()
    with pytest.raises(ValidationError):
        engine.deck(ReadingRequest(spread_id=SANMEIGAKU_SPREAD.id, deck_id="other"))
    with pytest.raises(ValidationError):
        engine.spread(ReadingRequest(spread_id="other", deck_id=SANMEIGAKU_DECK.id))


def test_no_top_level_core_leakage() -> None:
    import fortune_telling_core

    assert "sanmeigaku" not in fortune_telling_core.__all__


def _request(attrs: dict[str, str] | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=SANMEIGAKU_SPREAD.id,
        deck_id=SANMEIGAKU_DECK.id,
        querent=Querent("native", "Native", attrs or {"birth_datetime": _BIRTH}),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
    )
