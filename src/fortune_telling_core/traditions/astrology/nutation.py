"""Compatibility shim for shared astronomy nutation helpers."""

from fortune_telling_core.astronomy.nutation import (
    mean_obliquity,
    nutation_longitude,
    true_obliquity,
)

__all__ = ["mean_obliquity", "nutation_longitude", "true_obliquity"]
