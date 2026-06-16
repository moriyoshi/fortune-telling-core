"""Thai Thaksa graha (planet) data.

The eight Thaksa grahas (อัฏฐเคราะห์) are ordered in the canonical Thaksa
sequence — Sun, Moon, Mars, Mercury, Saturn, Jupiter, Rahu, Venus — which is
the order the planets are laid into the eight houses starting from a person's
birth-day ruler. Each graha carries its weekday rulership, lucky color,
day-of-birth Buddha posture (ปางประจำวัน), and planetary strength
(กำลังพระเคราะห์) used throughout Thai name and number divination.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Graha:
    """A Thaksa planet."""

    index: int
    """Position in the Thaksa cycle, 0=Sun through 7=Venus."""

    slug: str
    name: str
    thai: str
    color: str
    buddha_posture: str
    strength: int
    """Planetary strength (กำลังพระเคราะห์)."""

    @property
    def symbol_id(self) -> str:
        return f"thaksa.graha.{self.slug}"


# Ordered by the Thaksa cycle (Sun, Moon, Mars, Mercury, Saturn, Jupiter, Rahu, Venus).
GRAHAS: tuple[Graha, ...] = (
    Graha(0, "athit", "Sun", "อาทิตย์", "red", "Pang Thawai Net", 6),
    Graha(1, "chan", "Moon", "จันทร์", "cream", "Pang Ham Yat", 15),
    Graha(2, "angkhan", "Mars", "อังคาร", "pink", "Pang Saiyat", 8),
    Graha(3, "phut", "Mercury", "พุธ", "green", "Pang Um Bat", 17),
    Graha(4, "sao", "Saturn", "เสาร์", "black", "Pang Nak Prok", 10),
    Graha(5, "pharuehat", "Jupiter", "พฤหัสบดี", "orange", "Pang Samathi", 19),
    Graha(6, "rahu", "Rahu", "ราหู", "gray", "Pang Pa Lelai", 12),
    Graha(7, "suk", "Venus", "ศุกร์", "blue", "Pang Ramphueng", 21),
)

GRAHA_BY_SLUG = {graha.slug: graha for graha in GRAHAS}


def graha(index: int) -> Graha:
    """Return the graha at a Thaksa cycle position, wrapping modulo eight."""

    return GRAHAS[index % 8]
