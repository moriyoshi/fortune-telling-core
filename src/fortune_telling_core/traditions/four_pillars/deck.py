"""Four Pillars 22-symbol deck."""

from fortune_telling_core.symbols import Deck, Symbol
from fortune_telling_core.traditions.four_pillars.stems_branches import BRANCHES, STEMS

FOUR_PILLARS_DECK = Deck(
    id="fp.deck.ganzhi.v1",
    symbols=tuple(
        Symbol(
            id=f"fp.stem.{stem.slug}",
            name=f"{stem.cjk} {stem.slug.title()}",
            attributes={
                "kind": "stem",
                "cjk": stem.cjk,
                "element": stem.element.value,
                "polarity": stem.polarity.value,
            },
        )
        for stem in STEMS
    )
    + tuple(
        Symbol(
            id=f"fp.branch.{branch.slug}",
            name=f"{branch.cjk} {branch.animal}",
            attributes={
                "kind": "branch",
                "cjk": branch.cjk,
                "element": branch.element.value,
                "polarity": branch.polarity.value,
                "animal": branch.animal,
                "hidden_stems": ",".join(str(index) for index in branch.hidden_stems),
            },
        )
        for branch in BRANCHES
    ),
)
