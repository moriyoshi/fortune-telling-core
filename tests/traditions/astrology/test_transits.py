from datetime import UTC, datetime

from fortune_telling_core import Querent, ReadingRequest, reading_from_json, reading_to_json
from fortune_telling_core.astronomy.deltat import jd_tt_from_utc
from fortune_telling_core.astronomy.julian import julian_day_utc
from fortune_telling_core.traditions.astrology import (
    NATAL_CHART,
    TROPICAL_ZODIAC,
    FixedEphemeris,
    build_engine,
)
from fortune_telling_core.traditions.astrology.aspects import compute_cross_aspects
from fortune_telling_core.traditions.astrology.bodies import POSITION_NAMES, Body
from fortune_telling_core.traditions.astrology.ephemeris.protocol import Ephemeris
from fortune_telling_core.traditions.astrology.positions import EclipticPosition

_AS_OF = datetime(2026, 6, 16, tzinfo=UTC)
_BIRTH = datetime(1990, 1, 1, 12, tzinfo=UTC)


class RaisingEphemeris:
    id = "raising"
    version = "0"

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset(Body)

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        del body, jd_tt
        raise AssertionError("ephemeris must not be used during replay")


class _TwoTimeEphemeris:
    """Returns one position map before ``split_jd`` and another at/after it.

    Lets a test place natal bodies (at the birth Julian day) and transiting
    bodies (at the transit Julian day) at independently chosen longitudes, so a
    transit-to-natal aspect can be verified by hand.
    """

    id = "two-time"
    version = "0"

    def __init__(
        self,
        natal: dict[Body, float],
        transit: dict[Body, float],
        split_jd: float,
    ) -> None:
        self._natal = natal
        self._transit = transit
        self._split = split_jd

    def supported_bodies(self) -> frozenset[Body]:
        return frozenset(Body)

    def position(self, body: Body, jd_tt: float) -> EclipticPosition:
        chart = self._natal if jd_tt < self._split else self._transit
        if body not in chart and body is Body.SOUTH_NODE:
            return EclipticPosition((chart[Body.NORTH_NODE] + 180.0) % 360.0, 0.1)
        return EclipticPosition(chart[body], 1.0)


def test_compute_cross_aspects_orb_table_is_exact() -> None:
    # A single transiting body at 0 degrees against natal bodies placed at known
    # separations. Default orbs: conjunction/opposition 8, trine/square 6,
    # sextile 4 — each inclusive. 52 degrees matches nothing.
    natal = {
        f"natal {deg}": float(deg) for deg in (0, 5, 8, 52, 60, 64, 90, 96, 120, 126, 180, 188)
    }
    result = {
        a.second: (a.definition.id, round(a.orb, 2))
        for a in compute_cross_aspects({"transit X": 0.0}, natal)
    }
    assert result == {
        "natal 0": ("conjunction", 0.0),
        "natal 5": ("conjunction", 5.0),
        "natal 8": ("conjunction", 8.0),  # inclusive boundary
        "natal 60": ("sextile", 0.0),
        "natal 64": ("sextile", 4.0),  # inclusive boundary
        "natal 90": ("square", 0.0),
        "natal 96": ("square", 6.0),  # inclusive boundary
        "natal 120": ("trine", 0.0),
        "natal 126": ("trine", 6.0),  # inclusive boundary
        "natal 180": ("opposition", 0.0),
        "natal 188": ("opposition", 8.0),  # inclusive boundary
    }
    assert "natal 52" not in result  # outside every orb


def test_transits_are_computed_at_as_of_not_birth() -> None:
    # Natal and transit charts are identical except the Sun, which sits on the
    # natal Sun at birth but 90 degrees away at the transit time. A correct
    # engine reads the transit Sun from the as_of chart -> an exact square; a
    # bug that reused the birth time would report a conjunction instead.
    birth_jd = jd_tt_from_utc(julian_day_utc(_BIRTH))
    transit_jd = jd_tt_from_utc(julian_day_utc(_AS_OF))
    natal = {
        Body.SUN: 0.0,
        Body.MOON: 40.0,
        Body.MERCURY: 80.0,
        Body.VENUS: 130.0,
        Body.MARS: 170.0,
        Body.JUPITER: 210.0,
        Body.SATURN: 250.0,
        Body.URANUS: 290.0,
        Body.NEPTUNE: 330.0,
        Body.PLUTO: 20.0,
        Body.NORTH_NODE: 200.0,
    }
    transit = {**natal, Body.SUN: 90.0}
    ephemeris = _TwoTimeEphemeris(natal, transit, (birth_jd + transit_jd) / 2.0)

    summary = build_engine(ephemeris).cast(_request(_AS_OF)).summary or ""
    assert "transit Sun squares natal Sun (orb 0.00 degrees)" in summary
    assert "transit Sun conjunct natal Sun" not in summary


_ASPECT_TYPES = frozenset({"conjunction", "opposition", "trine", "square", "sextile"})
_VERBS = {
    "conjunction": "conjunct",
    "opposition": "opposes",
    "trine": "trines",
    "square": "squares",
    "sextile": "sextiles",
}


def test_natal_aspects_are_exposed_as_structured_extras() -> None:
    extras = build_engine(_fixed_ephemeris()).cast(_request()).draw.extras
    assert extras  # natal aspects always present
    for extra in extras:
        modifiers = extra.modifiers or {}
        assert extra.position_id == "aspect"
        assert extra.symbol_id.startswith("astro.aspect.")
        assert extra.symbol_id.removeprefix("astro.aspect.") in _ASPECT_TYPES
        assert set(modifiers) == {"first", "second", "orb", "kind"}
        assert modifiers["kind"] == "natal"  # no transits without as_of


def test_transit_aspects_are_exposed_as_structured_extras() -> None:
    extras = build_engine(_fixed_ephemeris()).cast(_request(_AS_OF)).draw.extras
    transit = [e for e in extras if (e.modifiers or {})["kind"] == "transit"]
    assert transit
    # The time-independent fixed ephemeris places each transiting body on its
    # natal longitude, so e.g. transit Sun is an exact conjunction to natal Sun.
    sun = next(
        e
        for e in transit
        if e.symbol_id == "astro.aspect.conjunction"
        and (e.modifiers or {})["first"] == "sun"
        and (e.modifiers or {})["second"] == "sun"
    )
    assert (sun.modifiers or {})["orb"] == "0.00"
    # The mirror node is excluded from the transiting set.
    assert all((e.modifiers or {})["first"] != "south_node" for e in transit)


def test_structured_aspects_are_consistent_with_the_summary() -> None:
    # Every structured aspect must be reflected verbatim in the freeform summary,
    # so the two representations never disagree.
    reading = build_engine().cast(_request(_AS_OF))  # built-in ephemeris
    summary = reading.summary or ""
    for extra in reading.draw.extras:
        modifiers = extra.modifiers or {}
        verb = _VERBS[extra.symbol_id.removeprefix("astro.aspect.")]
        orb = modifiers["orb"]
        if modifiers["kind"] == "natal":
            line = f"{modifiers['first']} {verb} {modifiers['second']} (orb {orb} degrees)"
        else:
            first = POSITION_NAMES[modifiers["first"]]
            second = POSITION_NAMES[modifiers["second"]]
            line = f"transit {first} {verb} natal {second} (orb {orb} degrees)"
        assert line in summary, line


def test_structured_extras_survive_serde_and_replay() -> None:
    request = _request(_AS_OF)
    reading = build_engine(_fixed_ephemeris()).cast(request)
    assert reading.draw.extras  # populated
    assert reading_from_json(reading_to_json(reading)).draw.extras == reading.draw.extras
    replayed = build_engine(RaisingEphemeris()).replay(request, reading.draw)
    assert replayed.draw.extras == reading.draw.extras


def test_no_as_of_keeps_a_pure_natal_chart() -> None:
    reading = build_engine(_fixed_ephemeris()).cast(_request())
    assert reading.summary is not None
    assert "Transits" not in reading.summary
    assert "transit_longitude" not in (reading.draw.selections[0].modifiers or {})
    assert all(not n.startswith("transit_at=") for n in reading.provenance.notes)


def test_as_of_adds_transit_to_natal_aspects() -> None:
    reading = build_engine(_fixed_ephemeris()).cast(_request(_AS_OF))
    assert reading.summary is not None
    # The fixed ephemeris is time-independent, so each transiting body sits on
    # its own natal longitude -> an exact (orb 0) conjunction.
    assert "Transits as of 2026-06-16T00:00:00+00:00" in reading.summary
    assert "transit Sun conjunct natal Sun (orb 0.00 degrees)" in reading.summary
    # The mirror node is excluded from the transiting set.
    assert "transit South Node" not in reading.summary
    assert "transit_at=2026-06-16T00:00:00+00:00" in reading.provenance.notes
    assert "transit_longitude" in (reading.draw.selections[0].modifiers or {})


def test_transit_replay_is_self_sufficient_without_ephemeris() -> None:
    request = _request(_AS_OF)
    reading = build_engine(_fixed_ephemeris()).cast(request)
    replayed = build_engine(RaisingEphemeris()).replay(request, reading.draw)
    assert replayed.draw == reading.draw
    assert replayed.summary == reading.summary
    assert reading_from_json(reading_to_json(reading)) == reading


def test_transit_cast_is_deterministic() -> None:
    engine = build_engine(_fixed_ephemeris())
    request = _request(_AS_OF)
    assert engine.cast(request) == engine.cast(request)


def _request(as_of: datetime | None = None) -> ReadingRequest:
    return ReadingRequest(
        spread_id=NATAL_CHART.id,
        deck_id=TROPICAL_ZODIAC.id,
        querent=Querent(
            id="native",
            display_name="Native",
            attributes={
                "birth_datetime": _BIRTH.isoformat(),
                "latitude": "0",
                "longitude": "0",
                "house_system": "whole_sign",
            },
        ),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
        as_of=as_of,
    )


def _fixed_ephemeris() -> Ephemeris:
    return FixedEphemeris(
        {
            Body.SUN: EclipticPosition(5.0, 1.0),
            Body.MOON: EclipticPosition(35.0, 13.0),
            Body.MERCURY: EclipticPosition(65.0, -1.0),
            Body.VENUS: EclipticPosition(95.0, 1.0),
            Body.MARS: EclipticPosition(125.0, 1.0),
            Body.JUPITER: EclipticPosition(155.0, 1.0),
            Body.SATURN: EclipticPosition(185.0, 1.0),
            Body.URANUS: EclipticPosition(215.0, 1.0),
            Body.NEPTUNE: EclipticPosition(245.0, 1.0),
            Body.PLUTO: EclipticPosition(275.0, 1.0),
            Body.NORTH_NODE: EclipticPosition(305.0, -0.1),
        }
    )
