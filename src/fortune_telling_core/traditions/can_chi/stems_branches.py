"""Vietnamese Can Chi stem and branch data.

The ten Thiên Can (heavenly stems) and twelve Địa Chi (earthly branches) are the
Vietnamese reflexes of the Sino-xenic sexagenary cycle. The branches carry the
twelve con giáp zodiac animals, which differ from the Chinese set most notably
in the Cat (Mèo) replacing the Rabbit and the Water Buffalo (Trâu) standing for
the Ox.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Can:
    """A Vietnamese heavenly stem (Thiên Can)."""

    index: int
    slug: str
    name: str
    element: str
    polarity: str

    @property
    def symbol_id(self) -> str:
        return f"cc.can.{self.slug}"


@dataclass(frozen=True, slots=True)
class Chi:
    """A Vietnamese earthly branch (Địa Chi)."""

    index: int
    slug: str
    name: str
    animal: str
    animal_vi: str
    element: str
    polarity: str

    @property
    def symbol_id(self) -> str:
        return f"cc.chi.{self.slug}"


_DUONG = "duong"  # Dương (yang)
_AM = "am"  # Âm (yin)

CANS: tuple[Can, ...] = (
    Can(0, "giap", "Giáp", "wood", _DUONG),
    Can(1, "at", "Ất", "wood", _AM),
    Can(2, "binh", "Bính", "fire", _DUONG),
    Can(3, "dinh", "Đinh", "fire", _AM),
    Can(4, "mau", "Mậu", "earth", _DUONG),
    Can(5, "ky", "Kỷ", "earth", _AM),
    Can(6, "canh", "Canh", "metal", _DUONG),
    Can(7, "tan", "Tân", "metal", _AM),
    Can(8, "nham", "Nhâm", "water", _DUONG),
    Can(9, "quy", "Quý", "water", _AM),
)

# Tý (Rat) and Tỵ (Snake) both romanise to "ty"; the snake uses the slug "ti"
# to keep symbol ids unique.
CHIS: tuple[Chi, ...] = (
    Chi(0, "ty", "Tý", "Rat", "Chuột", "water", _DUONG),
    Chi(1, "suu", "Sửu", "Water Buffalo", "Trâu", "earth", _AM),
    Chi(2, "dan", "Dần", "Tiger", "Hổ", "wood", _DUONG),
    Chi(3, "mao", "Mão", "Cat", "Mèo", "wood", _AM),
    Chi(4, "thin", "Thìn", "Dragon", "Rồng", "earth", _DUONG),
    Chi(5, "ti", "Tỵ", "Snake", "Rắn", "fire", _AM),
    Chi(6, "ngo", "Ngọ", "Horse", "Ngựa", "fire", _DUONG),
    Chi(7, "mui", "Mùi", "Goat", "Dê", "earth", _AM),
    Chi(8, "than", "Thân", "Monkey", "Khỉ", "metal", _DUONG),
    Chi(9, "dau", "Dậu", "Rooster", "Gà", "metal", _AM),
    Chi(10, "tuat", "Tuất", "Dog", "Chó", "earth", _DUONG),
    Chi(11, "hoi", "Hợi", "Pig", "Lợn", "water", _AM),
)

CAN_BY_SLUG = {can.slug: can for can in CANS}
CHI_BY_SLUG = {chi.slug: chi for chi in CHIS}


def can(index: int) -> Can:
    """Return the heavenly stem at a cycle position, wrapping modulo ten."""

    return CANS[index % 10]


def chi(index: int) -> Chi:
    """Return the earthly branch at a cycle position, wrapping modulo twelve."""

    return CHIS[index % 12]
