from datetime import UTC, datetime

from fortune_telling_core import Querent, ReadingRequest
from fortune_telling_core.astronomy.bodies import Body
from fortune_telling_core.astronomy.ephemeris.fixed import FixedEphemeris
from fortune_telling_core.astronomy.position import EclipticPosition
from fortune_telling_core.traditions import astrology, four_pillars, nine_star_ki

_NON_AMERICAN_SPELLINGS = (
    "analyse",
    "analysed",
    "analyses",
    "analysing",
    "behaviour",
    "centre",
    "centred",
    "colour",
    "colours",
    "emphasise",
    "emphasised",
    "emphasises",
    "emphasising",
    "favour",
    "favoured",
    "favours",
    "neighbour",
    "organise",
    "organised",
    "organises",
    "organising",
)


def test_generated_summaries_use_american_english() -> None:
    summaries = (
        _astrology_summary(),
        _four_pillars_summary(),
        _nine_star_ki_summary(),
    )

    for summary in summaries:
        assert summary is not None
        lower_summary = summary.lower()
        for spelling in _NON_AMERICAN_SPELLINGS:
            assert spelling not in lower_summary


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
