import pytest

from fortune_telling_core import (
    Querent,
    ReadingRequest,
    ValidationError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.astrology import (
    SUN_SIGN,
    TROPICAL_ZODIAC,
    build_engine,
)


def _request(**attributes: str) -> ReadingRequest:
    return ReadingRequest(
        spread_id=SUN_SIGN.id,
        deck_id=TROPICAL_ZODIAC.id,
        querent=Querent(id="native", display_name="Native", attributes=attributes),
    )


def test_sun_sign_from_birth_date() -> None:
    reading = build_engine().cast(_request(birth_date="1990-04-15"))

    assert len(reading.positions) == 1
    placement = reading.positions[0]
    assert placement.position.id == "sun"
    assert placement.symbol.id == "astro.sign.aries"
    modifiers = placement.selection.modifiers or {}
    assert modifiers["sign"] == "Aries"
    assert modifiers["element"] == "fire"
    assert modifiers["source"] == "date"
    assert modifiers["birth_date"] == "1990-04-15"
    assert reading.summary == "Sun sign Aries (fire, cardinal), Mar 21 – Apr 19."


def test_sun_sign_accepts_full_datetime() -> None:
    reading = build_engine().cast(_request(birth_datetime="1990-04-15T08:30:00+09:00"))

    assert reading.positions[0].symbol.id == "astro.sign.aries"
    assert (reading.positions[0].selection.modifiers or {})["birth_date"] == "1990-04-15"


def test_explicit_sun_sign_needs_no_date() -> None:
    reading = build_engine().cast(_request(sun_sign="scorpio"))

    placement = reading.positions[0]
    assert placement.symbol.id == "astro.sign.scorpio"
    modifiers = placement.selection.modifiers or {}
    assert modifiers["source"] == "explicit"
    assert "birth_date" not in modifiers
    assert reading.summary == "Sun sign Scorpio (water, fixed), Oct 23 – Nov 21."


def test_explicit_sun_sign_accepts_symbol_id() -> None:
    reading = build_engine().cast(_request(sun_sign="astro.sign.leo"))

    assert reading.positions[0].symbol.id == "astro.sign.leo"


def test_sun_sign_is_tropical_and_rng_free() -> None:
    reading = build_engine().cast(_request(birth_date="1990-04-15"))

    assert reading.draw.deck_id == TROPICAL_ZODIAC.id
    assert reading.provenance.rng_kind is None
    assert "zodiac=tropical" in reading.provenance.notes
    assert "sun_sign_source=date" in reading.provenance.notes


def test_sun_sign_is_deterministic() -> None:
    request = _request(birth_date="1990-04-15")
    engine = build_engine()

    assert engine.cast(request) == engine.cast(request)


def test_sun_sign_replays_and_round_trips() -> None:
    request = _request(sun_sign="gemini")
    engine = build_engine()
    reading = engine.cast(request)

    assert engine.replay(request, reading.draw) == reading
    assert reading_from_json(reading_to_json(reading)) == reading


def test_missing_input_raises() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request())


def test_unknown_sign_raises() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request(sun_sign="ophiuchus"))


def test_malformed_date_raises() -> None:
    with pytest.raises(ValidationError):
        build_engine().cast(_request(birth_date="not-a-date"))
