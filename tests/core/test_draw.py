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
