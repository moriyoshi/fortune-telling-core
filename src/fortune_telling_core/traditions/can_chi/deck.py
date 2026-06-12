"""Can Chi deck: ten Thiên Can and twelve Địa Chi."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.can_chi.stems_branches import CANS, CHIS

CAN_CHI_DECK = Deck(
    id="cc.deck.canchi.v1",
    symbols=(
        *(
            Symbol(
                id=can.symbol_id,
                name=can.name,
                attributes={
                    "kind": "can",
                    "slug": can.slug,
                    "cycle_index": str(can.index),
                    "element": can.element,
                    "polarity": can.polarity,
                },
            )
            for can in CANS
        ),
        *(
            Symbol(
                id=chi.symbol_id,
                name=chi.name,
                attributes={
                    "kind": "chi",
                    "slug": chi.slug,
                    "cycle_index": str(chi.index),
                    "animal": chi.animal,
                    "animal_vi": chi.animal_vi,
                    "element": chi.element,
                    "polarity": chi.polarity,
                },
            )
            for chi in CHIS
        ),
    ),
)
