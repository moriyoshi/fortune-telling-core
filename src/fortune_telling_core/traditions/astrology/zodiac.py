"""Zodiac sign decks."""

from __future__ import annotations

from fortune_telling_core.symbols import Deck, Symbol

_SIGNS = (
    ("aries", "Aries", "fire", "cardinal", "positive", "Mars"),
    ("taurus", "Taurus", "earth", "fixed", "negative", "Venus"),
    ("gemini", "Gemini", "air", "mutable", "positive", "Mercury"),
    ("cancer", "Cancer", "water", "cardinal", "negative", "Moon"),
    ("leo", "Leo", "fire", "fixed", "positive", "Sun"),
    ("virgo", "Virgo", "earth", "mutable", "negative", "Mercury"),
    ("libra", "Libra", "air", "cardinal", "positive", "Venus"),
    ("scorpio", "Scorpio", "water", "fixed", "negative", "Mars"),
    ("sagittarius", "Sagittarius", "fire", "mutable", "positive", "Jupiter"),
    ("capricorn", "Capricorn", "earth", "cardinal", "negative", "Saturn"),
    ("aquarius", "Aquarius", "air", "fixed", "positive", "Saturn"),
    ("pisces", "Pisces", "water", "mutable", "negative", "Jupiter"),
)


def _symbols() -> tuple[Symbol, ...]:
    return tuple(
        Symbol(
            id=f"astro.sign.{slug}",
            name=name,
            attributes={
                "element": element,
                "modality": modality,
                "polarity": polarity,
                "ruler": ruler,
                "order": str(index + 1),
            },
        )
        for index, (slug, name, element, modality, polarity, ruler) in enumerate(_SIGNS)
    )


TROPICAL_ZODIAC = Deck(id="astro.zodiac.tropical.v1", symbols=_symbols())
SIDEREAL_ZODIAC = Deck(id="astro.zodiac.sidereal.v1", symbols=_symbols())
