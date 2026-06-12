"""Petit Lenormand 36-card deck as generic Symbol data.

The thirty-six cards are numbered in their traditional order from 1 (Rider) to
36 (Cross). Playing-card insets are intentionally omitted: they vary between
publishers, so only the universal number and name identify each card here.
"""

from __future__ import annotations

from fortune_telling_core.symbols import Deck, Symbol

# (number, slug, name) in the canonical Lenormand order.
_CARDS: tuple[tuple[int, str, str], ...] = (
    (1, "rider", "Rider"),
    (2, "clover", "Clover"),
    (3, "ship", "Ship"),
    (4, "house", "House"),
    (5, "tree", "Tree"),
    (6, "clouds", "Clouds"),
    (7, "snake", "Snake"),
    (8, "coffin", "Coffin"),
    (9, "bouquet", "Bouquet"),
    (10, "scythe", "Scythe"),
    (11, "whip", "Whip"),
    (12, "birds", "Birds"),
    (13, "child", "Child"),
    (14, "fox", "Fox"),
    (15, "bear", "Bear"),
    (16, "stars", "Stars"),
    (17, "stork", "Stork"),
    (18, "dog", "Dog"),
    (19, "tower", "Tower"),
    (20, "garden", "Garden"),
    (21, "mountain", "Mountain"),
    (22, "crossroads", "Crossroads"),
    (23, "mice", "Mice"),
    (24, "heart", "Heart"),
    (25, "ring", "Ring"),
    (26, "book", "Book"),
    (27, "letter", "Letter"),
    (28, "man", "Man"),
    (29, "woman", "Woman"),
    (30, "lily", "Lily"),
    (31, "sun", "Sun"),
    (32, "moon", "Moon"),
    (33, "key", "Key"),
    (34, "fish", "Fish"),
    (35, "anchor", "Anchor"),
    (36, "cross", "Cross"),
)

LENORMAND_DECK = Deck(
    id="lenormand.deck.petit.v1",
    symbols=tuple(
        Symbol(
            id=f"lenormand.card.{slug}",
            name=name,
            attributes={"number": str(number), "slug": slug},
        )
        for number, slug, name in _CARDS
    ),
)
