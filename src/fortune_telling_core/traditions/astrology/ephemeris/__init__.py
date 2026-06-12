"""Compatibility shims for shared ephemeris implementations."""

from fortune_telling_core.astronomy.ephemeris.builtin import BuiltinEphemeris
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.ephemeris.protocol import Ephemeris

__all__ = ["BuiltinEphemeris", "Ephemeris", "FixedEphemeris"]
