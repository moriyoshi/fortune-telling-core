"""Zodiac signs and sign decks."""

from __future__ import annotations

from enum import StrEnum

from fortune_telling_core.symbols import Deck, Symbol


class Sign(StrEnum):
    """The twelve zodiac signs in canonical Aries-to-Pisces order.

    Members are the lowercase slugs used throughout the package. This enum is
    the single source of truth for the set of signs and their order; sign decks,
    longitude-to-sign lookups and date ranges all derive from it.
    """

    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"

    @property
    def ordinal(self) -> int:
        """Zero-based position in the zodiac (Aries is 0, Pisces is 11)."""
        return _SIGN_ORDINAL[self]

    @property
    def symbol_id(self) -> str:
        """Deck symbol id for this sign, e.g. ``astro.sign.aries``."""
        return f"astro.sign.{self.value}"

    @property
    def display_name(self) -> str:
        """Capitalized English display name, e.g. ``Aries``."""
        return self.value.capitalize()


_SIGN_ORDINAL = {sign: ordinal for ordinal, sign in enumerate(Sign)}

# Per-sign (element, modality, polarity, ruler), keyed by sign.
_ATTRIBUTES: dict[Sign, tuple[str, str, str, str]] = {
    Sign.ARIES: ("fire", "cardinal", "positive", "Mars"),
    Sign.TAURUS: ("earth", "fixed", "negative", "Venus"),
    Sign.GEMINI: ("air", "mutable", "positive", "Mercury"),
    Sign.CANCER: ("water", "cardinal", "negative", "Moon"),
    Sign.LEO: ("fire", "fixed", "positive", "Sun"),
    Sign.VIRGO: ("earth", "mutable", "negative", "Mercury"),
    Sign.LIBRA: ("air", "cardinal", "positive", "Venus"),
    Sign.SCORPIO: ("water", "fixed", "negative", "Mars"),
    Sign.SAGITTARIUS: ("fire", "mutable", "positive", "Jupiter"),
    Sign.CAPRICORN: ("earth", "cardinal", "negative", "Saturn"),
    Sign.AQUARIUS: ("air", "fixed", "positive", "Saturn"),
    Sign.PISCES: ("water", "mutable", "negative", "Jupiter"),
}


def _symbols() -> tuple[Symbol, ...]:
    symbols: list[Symbol] = []
    for sign in Sign:
        element, modality, polarity, ruler = _ATTRIBUTES[sign]
        symbols.append(
            Symbol(
                id=sign.symbol_id,
                name=sign.display_name,
                attributes={
                    "element": element,
                    "modality": modality,
                    "polarity": polarity,
                    "ruler": ruler,
                    "order": str(sign.ordinal + 1),
                },
            )
        )
    return tuple(symbols)


TROPICAL_ZODIAC = Deck(id="astro.zodiac.tropical.v1", symbols=_symbols())
SIDEREAL_ZODIAC = Deck(id="astro.zodiac.sidereal.v1", symbols=_symbols())
