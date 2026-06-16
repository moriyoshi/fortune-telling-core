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

# 1984-02-02 is a 丙寅 day. At noon JST the year pillar is the pre-立春 癸亥 and
# the month pillar 乙丑, giving a stable reference chart.
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
    # Day pillar 丙寅: centre 主星 from 寅 (元命 甲) is 龍高星.
    assert by_position["day_branch"].symbol_id == "sanmeigaku.main.ryuko"
    assert by_position["day_branch"].modifiers is not None
    assert by_position["day_branch"].modifiers["day_master"] == "丙"
    # 従星 of 丙 at 寅 (長生) is 天貴星.
    assert by_position["day_branch_subordinate"].symbol_id == "sanmeigaku.subordinate.tenki"
    assert reading.summary is not None
    assert "龍高星" in reading.summary


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


def test_annual_year_un_uses_as_of_and_needs_no_gender() -> None:
    # 2024 is 甲辰 (an externally fixed sexagenary year). Day master is 丙 (the
    # 1984-02-02 丙寅 day), so 甲 → 主星 龍高星 and 辰 → 従星 天南星.
    request = ReadingRequest(
        spread_id=SANMEIGAKU_SPREAD.id,
        deck_id=SANMEIGAKU_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": _BIRTH}),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
        as_of=datetime(2024, 3, 1, tzinfo=UTC),
    )
    reading = build_engine().cast(request)
    assert reading.summary is not None
    assert "Annual 2024 甲辰: 主星 龍高星, 従星 天南星." in reading.summary
    # No gender → no 大運 section.
    assert "Daiun" not in reading.summary


def test_target_year_option_overrides_as_of_for_annual() -> None:
    attrs = {"birth_datetime": _BIRTH, "target_year": "2024"}
    request = ReadingRequest(
        spread_id=SANMEIGAKU_SPREAD.id,
        deck_id=SANMEIGAKU_DECK.id,
        querent=Querent("native", "Native", attrs),
        as_of=datetime(2030, 1, 1, tzinfo=UTC),
    )
    assert "Annual 2024 甲辰" in (build_engine().cast(request).summary or "")


def test_daiun_direction_follows_year_polarity_and_gender() -> None:
    # The pre-立春 year pillar here is 癸亥 (陰年). 陰年男性 → 逆行, so the first
    # 大運 column retreats from the 乙丑 month pillar to 甲子; 陰年女性 → 順行,
    # advancing to 丙寅.
    male = build_engine(luck_count=2).cast(_request({"birth_datetime": _BIRTH, "gender": "male"}))
    female = build_engine(luck_count=2).cast(
        _request({"birth_datetime": _BIRTH, "gender": "female"})
    )
    assert male.summary is not None and female.summary is not None
    assert "Daiun (backward): 甲子@" in male.summary
    assert "Daiun (forward): 丙寅@" in female.summary


def test_gendered_cast_replay_and_serde_are_deterministic() -> None:
    request = _request({"birth_datetime": _BIRTH, "gender": "male"})
    reading = build_engine().cast(request)
    replayed = build_engine().replay(request, reading.draw)

    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert "Daiun" in (reading.summary or "")
    assert reading_from_json(reading_to_json(reading)) == reading
    assert "daiun_start_age=jie_days/3" in reading.provenance.notes


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
