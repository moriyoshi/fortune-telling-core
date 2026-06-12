import json

import pytest

from fortune_telling_core import (
    RandomRng,
    ReadingRequest,
    SchemaVersionError,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.traditions.tarot import RWS_DECK, SINGLE_CARD, build_engine


def test_unknown_future_schema_version_raises() -> None:
    request = _request()
    reading = build_engine().read(request, rng=RandomRng(1))
    data = json.loads(reading_to_json(reading))
    data["schema_version"] = 999

    with pytest.raises(SchemaVersionError):
        reading_from_json(json.dumps(data))


def test_additive_fields_are_tolerated() -> None:
    reading = build_engine().read(_request(), rng=RandomRng(1))
    data = json.loads(reading_to_json(reading))
    data["future_field"] = "ignored"
    data["request"]["future_field"] = "ignored"

    assert reading_from_json(json.dumps(data)) == reading


def _request() -> ReadingRequest:
    return ReadingRequest(
        spread_id=SINGLE_CARD.id,
        deck_id=RWS_DECK.id,
    )
