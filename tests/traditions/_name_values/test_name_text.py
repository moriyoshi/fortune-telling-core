import pytest

from fortune_telling_core import ValidationError
from fortune_telling_core.traditions._name_text import (
    NameValueUnit,
    format_value_trace,
    is_ignorable,
    parse_value_trace,
    strip_combining_marks,
)


def test_value_trace_round_trip() -> None:
    units = (NameValueUnit("י", 10), NameValueUnit("ם", 40))
    text = format_value_trace(units)
    assert text == "י:10,ם:40"
    assert parse_value_trace(text) == units


def test_parse_empty_trace() -> None:
    assert parse_value_trace("") == ()


@pytest.mark.parametrize("bad", ["abc", ":5", "a:", "a:x"])
def test_parse_rejects_malformed_trace(bad: str) -> None:
    with pytest.raises(ValidationError):
        parse_value_trace(bad)


def test_strip_combining_marks_removes_niqqud() -> None:
    # shin + sin-dot + qamats decomposes to base letters only.
    assert strip_combining_marks("שָׁלוֹם") == "שלום"
    assert strip_combining_marks("José") == "Jose"


def test_is_ignorable() -> None:
    assert is_ignorable(" ")
    assert is_ignorable("-")
    assert is_ignorable(".")
    assert not is_ignorable("A")
    assert not is_ignorable("א")
