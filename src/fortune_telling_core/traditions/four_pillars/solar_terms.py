"""Compatibility shim for shared solar-term helpers."""

from fortune_telling_core.astronomy.solar_terms import (
    JIE_LONGITUDES,
    adjacent_jie_crossing,
    lichun_crossing,
    solar_month_index,
    solar_term_crossing,
)

months_since_yin = solar_month_index


def month_branch_index(solar_longitude_value: float) -> int:
    return (2 + solar_month_index(solar_longitude_value)) % 12


__all__ = [
    "JIE_LONGITUDES",
    "adjacent_jie_crossing",
    "lichun_crossing",
    "month_branch_index",
    "months_since_yin",
    "solar_month_index",
    "solar_term_crossing",
]
