"""Deterministic test ephemeris."""

from collections.abc import Mapping

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.errors import EphemerisError
from fortune_telling_core.astronomy.position import EclipticPosition


class FixedEphemeris:
    """Deterministic ephemeris backed by a fixed position mapping.

    This backend is intended for tests, examples, and replay fixtures where
    the caller wants exact symbolic placements without astronomical
    calculation.

    Args:
        positions: Mapping from body identifiers to ecliptic positions. If a
            north node is supplied without a south node, the south node is
            derived as the opposite longitude.

    Example:
        ```python
        from fortune_telling_core.astronomy import Body, EclipticPosition, FixedEphemeris

        ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(10.0)})
        assert ephemeris.position(Body.SUN, 0.0).longitude == 10.0
        ```
    """

    id = "astro.ephemeris.fixed"
    version = "0.1.0"

    def __init__(self, positions: Mapping[Body, EclipticPosition]) -> None:
        self._positions = dict(positions)
        if Body.NORTH_NODE in self._positions and Body.SOUTH_NODE not in self._positions:
            north = self._positions[Body.NORTH_NODE]
            self._positions[Body.SOUTH_NODE] = EclipticPosition(
                north.longitude + 180.0, north.speed
            )

    def supported_bodies(self) -> frozenset[Body]:
        """Return the bodies present in the fixed mapping."""

        return frozenset(self._positions)

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        """Return the fixed position for a body.

        Args:
            body: Body to look up.
            jd_tt: Ignored Julian day, accepted for protocol compatibility.

        Returns:
            The configured ecliptic position.

        Raises:
            EphemerisError: If no position exists for ``body``.
        """

        del jd_tt
        value = self._positions.get(body)
        if value is None:
            raise EphemerisError(f"fixed ephemeris has no position for {body}")
        return value
