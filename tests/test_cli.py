from __future__ import annotations

import json
from datetime import datetime

from pytest import CaptureFixture

from fortune_telling_core.cli import main


def test_cli_text_demo_outputs_tarot(capsys: CaptureFixture[str]) -> None:
    assert main(["tarot", "--seed", "7"]) == 0

    output = capsys.readouterr().out

    assert "Tarot" in output
    assert "Engine: tarot.rws.engine@0.1.0" in output
    assert "Replay artifact: 3 recorded selections" in output
    assert "Positions:" in output


def test_cli_json_demo_outputs_serialized_reading(capsys: CaptureFixture[str]) -> None:
    assert main(["nine-star-ki", "--json", "--target-year", "2026"]) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["provenance"]["engine_id"] == "ninestarki.engine"
    assert "locale" not in payload["request"]
    assert "interpretation_data_id" not in payload["provenance"]
    assert payload["request"]["options"]["target_year"] == "2026"
    assert payload["draw"]["selections"]


def test_cli_naive_birth_datetime_is_made_timezone_aware(
    capsys: CaptureFixture[str],
) -> None:
    assert main(["astrology", "--json", "--birth-datetime", "1990-01-01T12:00:00"]) == 0

    payload = json.loads(capsys.readouterr().out)
    birth_datetime = payload["request"]["querent"]["attributes"]["birth_datetime"]

    parsed = datetime.fromisoformat(birth_datetime)
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() is not None
