import pytest

from fortune_telling_core import Draw, Selection, ValidationError


def test_draw_validates_one_selection_per_position() -> None:
    with pytest.raises(ValidationError):
        Draw(deck_id="deck", spread_id="spread", selections=())
    with pytest.raises(ValidationError):
        Draw(
            deck_id="deck",
            spread_id="spread",
            selections=(
                Selection(position_id="focus", symbol_id="one"),
                Selection(position_id="focus", symbol_id="two"),
            ),
        )


def test_draw_preserves_selection_order_and_modifiers() -> None:
    draw = Draw(
        deck_id="deck",
        spread_id="spread",
        selections=(
            Selection(position_id="past", symbol_id="one", modifiers={"orientation": "upright"}),
            Selection(position_id="present", symbol_id="two"),
        ),
    )

    assert [selection.position_id for selection in draw.selections] == ["past", "present"]
    assert draw.selections[0].modifiers == {"orientation": "upright"}


def test_draw_extras_default_empty_and_omitted_from_serialization() -> None:
    draw = Draw(deck_id="deck", spread_id="spread", selections=(Selection("focus", "one"),))
    assert draw.extras == ()
    # No churn for traditions that do not use extras.
    assert "extras" not in draw.to_dict()
    assert Draw.from_dict(draw.to_dict()) == draw


def test_draw_extras_round_trip_and_allow_repeated_position_ids() -> None:
    # extras carry no per-position uniqueness contract (unlike selections).
    draw = Draw(
        deck_id="deck",
        spread_id="spread",
        selections=(Selection("focus", "one"),),
        extras=(
            Selection("aspect", "astro.aspect.trine", {"first": "sun", "second": "moon"}),
            Selection("aspect", "astro.aspect.square", {"first": "mars", "second": "venus"}),
        ),
    )

    assert [extra.symbol_id for extra in draw.extras] == [
        "astro.aspect.trine",
        "astro.aspect.square",
    ]
    serialized = draw.to_dict()
    extras = serialized["extras"]
    assert isinstance(extras, list)
    assert len(extras) == 2
    assert Draw.from_dict(serialized) == draw
