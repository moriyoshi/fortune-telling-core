from datetime import UTC, datetime

from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.position import EclipticPosition
from fortune_telling_core.traditions import (
    astrology,
    four_pillars,
    koyomi,
    nine_star_ki,
    sanmeigaku,
    thaksa,
    zi_wei,
)
from fortune_telling_core.traditions.thaksa.grahas import GRAHAS

_NON_AMERICAN_SPELLINGS = (
    "analyse",
    "analysed",
    "analyses",
    "analysing",
    "behaviour",
    "calibre",
    "catalogue",
    "centre",
    "centred",
    "colour",
    "colours",
    "defence",
    "dialogue",
    "emphasise",
    "emphasised",
    "emphasises",
    "emphasising",
    "favour",
    "favoured",
    "favours",
    "fibre",
    "fulfil",
    "grey",
    "honour",
    "labelled",
    "labelling",
    "licence",
    "metre",
    "modelled",
    "neighbour",
    "offence",
    "organise",
    "organised",
    "organises",
    "organising",
    "travelled",
)


def test_generated_summaries_use_american_english() -> None:
    summaries = (
        _astrology_summary(),
        _four_pillars_summary(),
        _nine_star_ki_summary(),
        _sanmeigaku_summary(),
        _thaksa_summary(),
        _zi_wei_summary(),
        _koyomi_summary(),
    )

    for summary in summaries:
        assert summary is not None
        lower_summary = summary.lower()
        for spelling in _NON_AMERICAN_SPELLINGS:
            assert spelling not in lower_summary


def test_thaksa_graha_colors_are_american_english() -> None:
    # The ruling graha's color surfaces in the summary, so a British color value
    # (e.g. "grey") would slip past templates regardless of the birth day. Guard
    # the data directly.
    for graha in GRAHAS:
        assert graha.color not in _NON_AMERICAN_SPELLINGS, graha.color


def _astrology_summary() -> str | None:
    request = ReadingRequest(
        spread_id=astrology.NATAL_CHART.id,
        deck_id=astrology.TROPICAL_ZODIAC.id,
        querent=Querent(
            id="native",
            display_name="Native",
            attributes={
                "birth_datetime": datetime(1990, 1, 1, 12, tzinfo=UTC).isoformat(),
                "latitude": "0",
                "longitude": "0",
                "house_system": "whole_sign",
            },
        ),
    )
    ephemeris = astrology.FixedEphemeris(
        {body: EclipticPosition(float(index * 30), 1.0) for index, body in enumerate(Body)}
    )
    return astrology.build_engine(ephemeris).cast(request).summary


def _four_pillars_summary() -> str | None:
    request = ReadingRequest(
        spread_id=four_pillars.FOUR_PILLARS_SPREAD.id,
        deck_id=four_pillars.FOUR_PILLARS_DECK.id,
        querent=Querent(
            "native",
            "Native",
            {
                "birth_datetime": "1984-02-02T00:30:00+00:00",
                "latitude": "0",
                "longitude": "0",
                "gender": "male",
                "target_year": "2024",
                "luck_count": "3",
            },
        ),
    )
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(320.0, 1.0)})
    return four_pillars.build_engine(ephemeris).cast(request).summary


def _nine_star_ki_summary() -> str | None:
    request = ReadingRequest(
        spread_id=nine_star_ki.NINE_STAR_KI_SPREAD.id,
        deck_id=nine_star_ki.NINE_STAR_KI_DECK.id,
        querent=Querent(
            "native",
            "Native",
            {
                "birth_datetime": "2024-02-05T00:00:00+00:00",
                "latitude": "0",
                "longitude": "0",
                "target_year": "2024",
            },
        ),
        requested_at=datetime(2026, 6, 12, tzinfo=UTC),
    )
    ephemeris = FixedEphemeris({Body.SUN: EclipticPosition(315.0, 1.0)})
    return nine_star_ki.build_engine(ephemeris).cast(request).summary


def _sanmeigaku_summary() -> str | None:
    # gender exercises the 大運 luck-cycle branch in addition to 年運.
    request = ReadingRequest(
        spread_id=sanmeigaku.SANMEIGAKU_SPREAD.id,
        deck_id=sanmeigaku.SANMEIGAKU_DECK.id,
        querent=Querent(
            "native",
            "Native",
            {"birth_datetime": "1984-02-02T12:00:00+09:00", "gender": "female"},
        ),
        requested_at=datetime(2024, 6, 1, tzinfo=UTC),
    )
    return sanmeigaku.build_engine().cast(request).summary


def _thaksa_summary() -> str | None:
    # A Wednesday birth at/after 18:00 rules under Rahu, whose lucky color is the
    # one most at risk of a British spelling ("gray").
    request = ReadingRequest(
        spread_id=thaksa.THAKSA_SPREAD.id,
        deck_id=thaksa.THAKSA_DECK.id,
        querent=Querent("native", "Native", {"birth_datetime": "1990-01-03T20:00:00+07:00"}),
    )
    return thaksa.build_engine().cast(request).summary


def _zi_wei_summary() -> str | None:
    request = ReadingRequest(
        spread_id=zi_wei.ZI_WEI_SPREAD.id,
        deck_id=zi_wei.ZI_WEI_DECK.id,
        querent=Querent(
            "native",
            "Native",
            {"birth_datetime": "1985-04-29T10:00:00+08:00", "gender": "male"},
        ),
        requested_at=datetime(2026, 6, 15, tzinfo=UTC),
    )
    return zi_wei.build_engine().cast(request).summary


def _koyomi_summary() -> str | None:
    request = ReadingRequest(
        spread_id=koyomi.KOYOMI_SPREAD.id,
        deck_id=koyomi.KOYOMI_DECK.id,
        querent=Querent("native", "Native", {"target_datetime": "2024-01-01T12:00:00+09:00"}),
    )
    return koyomi.build_engine().cast(request).summary
