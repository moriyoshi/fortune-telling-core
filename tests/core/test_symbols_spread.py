from collections.abc import Sequence
from typing import cast

import pytest

from fortune_telling_core import Deck, Position, Spread, Symbol, ValidationError


def test_deck_validates_empty_duplicate_and_weight_length() -> None:
    symbol = Symbol(id="one", name="One")

    with pytest.raises(ValidationError):
        Deck(id="empty", symbols=())
    with pytest.raises(ValidationError):
        Deck(id="dupe", symbols=(symbol, symbol))
    with pytest.raises(ValidationError):
        Deck(id="weights", symbols=(symbol,), weights=(1, 2))
    with pytest.raises(ValidationError):
        Deck(id="float-weights", symbols=(symbol,), weights=cast(Sequence[int], (1.5,)))


def test_deck_normalises_attributes_and_weights() -> None:
    deck = Deck(
        id="deck",
        symbols=(Symbol(id="one", name="One", attributes={"kind": "test"}),),
        weights=[2],
    )

    assert deck.symbols[0].attributes == {"kind": "test"}
    assert deck.weights == (2,)


def test_spread_validates_empty_and_duplicate_positions() -> None:
    position = Position(id="focus", name="Focus")

    with pytest.raises(ValidationError):
        Spread(id="empty", name="Empty", positions=())
    with pytest.raises(ValidationError):
        Spread(id="dupe", name="Dupe", positions=(position, position))


def test_spread_size() -> None:
    spread = Spread(
        id="spread",
        name="Spread",
        positions=(Position(id="a", name="A"), Position(id="b", name="B")),
    )

    assert spread.size == 2
