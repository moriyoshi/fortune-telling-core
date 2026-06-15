"""Zi Wei Dou Shu deck: the twelve earthly-branch chart positions.

A Zi Wei chart assigns the twelve palaces to the twelve earthly branches and
populates them with stars. Each palace selection's symbol is the branch the
palace occupies; the stars are carried as selection modifiers.
"""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.zi_wei.chart import BRANCH_CJK, BRANCH_SLUG

ZI_WEI_DECK = Deck(
    id="zi_wei.deck.branches.v1",
    symbols=tuple(
        Symbol(
            id=f"zi_wei.branch.{slug}",
            name=BRANCH_CJK[index],
            attributes={"cjk": BRANCH_CJK[index], "index": str(index)},
        )
        for index, slug in enumerate(BRANCH_SLUG)
    ),
)
