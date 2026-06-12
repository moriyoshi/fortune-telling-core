"""Rider-Waite-Smith tarot deck as generic Symbol data."""

from __future__ import annotations

from fortune_telling_core.symbols import Deck, Symbol

_MAJOR_ARCANA = (
    ("the_fool", "The Fool", "0"),
    ("the_magician", "The Magician", "1"),
    ("the_high_priestess", "The High Priestess", "2"),
    ("the_empress", "The Empress", "3"),
    ("the_emperor", "The Emperor", "4"),
    ("the_hierophant", "The Hierophant", "5"),
    ("the_lovers", "The Lovers", "6"),
    ("the_chariot", "The Chariot", "7"),
    ("strength", "Strength", "8"),
    ("the_hermit", "The Hermit", "9"),
    ("wheel_of_fortune", "Wheel of Fortune", "10"),
    ("justice", "Justice", "11"),
    ("the_hanged_man", "The Hanged Man", "12"),
    ("death", "Death", "13"),
    ("temperance", "Temperance", "14"),
    ("the_devil", "The Devil", "15"),
    ("the_tower", "The Tower", "16"),
    ("the_star", "The Star", "17"),
    ("the_moon", "The Moon", "18"),
    ("the_sun", "The Sun", "19"),
    ("judgement", "Judgement", "20"),
    ("the_world", "The World", "21"),
)

_MINOR_SUITS = ("wands", "cups", "swords", "pentacles")
_MINOR_RANKS = (
    ("ace", "Ace", "1"),
    ("two", "Two", "2"),
    ("three", "Three", "3"),
    ("four", "Four", "4"),
    ("five", "Five", "5"),
    ("six", "Six", "6"),
    ("seven", "Seven", "7"),
    ("eight", "Eight", "8"),
    ("nine", "Nine", "9"),
    ("ten", "Ten", "10"),
    ("page", "Page", "page"),
    ("knight", "Knight", "knight"),
    ("queen", "Queen", "queen"),
    ("king", "King", "king"),
)


def _major_symbols() -> tuple[Symbol, ...]:
    return tuple(
        Symbol(
            id=f"tarot.rws.major.{slug}",
            name=name,
            attributes={"arcana": "major", "number": number},
        )
        for slug, name, number in _MAJOR_ARCANA
    )


def _minor_symbols() -> tuple[Symbol, ...]:
    return tuple(
        Symbol(
            id=f"tarot.rws.minor.{suit}.{rank_slug}",
            name=f"{rank_name} of {suit.title()}",
            attributes={"arcana": "minor", "suit": suit, "rank": rank_value},
        )
        for suit in _MINOR_SUITS
        for rank_slug, rank_name, rank_value in _MINOR_RANKS
    )


RWS_DECK = Deck(id="tarot.rws.v1", symbols=_major_symbols() + _minor_symbols())
