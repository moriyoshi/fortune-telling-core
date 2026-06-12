"""Shared ephemeris protocol."""

from typing import Protocol

from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.position import EclipticPosition


class Ephemeris(Protocol):
    """Protocol for injectable astronomy backends.

    Implementations provide apparent geocentric ecliptic positions in degrees.
    Latitude may be ``None`` when a backend or body does not compute it. The
    fortune-telling traditions depend only on this protocol, so applications
    can bring their own precision and licensing choices.

    Attributes:
        id: Stable backend identifier recorded in reading provenance.
        version: Backend version recorded in reading provenance.
    """

    id: str
    version: str

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        """Return an apparent geocentric ecliptic position.

        Args:
            body: Body to compute.
            jd_tt: Julian day on the Terrestrial Time scale.

        Returns:
            Ecliptic position for the requested body.

        Raises:
            EphemerisError: If the backend cannot compute the requested body.
        """

    def supported_bodies(self) -> frozenset[Body]:
        """Return the bodies supported by this ephemeris."""
