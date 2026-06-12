"""Command-line demonstrations for the bundled tradition engines."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from fortune_telling_core import Querent, RandomRng, Reading, ReadingRequest
from fortune_telling_core.traditions import astrology, four_pillars, nine_star_ki, tarot

_DEMO_REQUESTED_AT = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
_DEFAULT_BIRTH_DATETIME = "1990-01-01T12:00:00+00:00"
_DEFAULT_LATITUDE = "51.5074"
_DEFAULT_LONGITUDE = "-0.1278"
_DEFAULT_TARGET_YEAR = 2026


@dataclass(frozen=True, slots=True)
class _Demo:
    key: str
    title: str
    build: Callable[[argparse.Namespace], Reading]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the demo CLI.

    Args:
        argv: Optional argument vector. When omitted, ``sys.argv`` is used.

    Returns:
        Process exit status.
    """

    parser = _build_parser()
    args = parser.parse_args(argv)
    demos = _selected_demos(args.demo)
    readings = [demo.build(args) for demo in demos]
    if args.json:
        payload: object = (
            readings[0].to_dict()
            if len(readings) == 1
            else [reading.to_dict() for reading in readings]
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    print(_render_readings(tuple(zip(demos, readings, strict=True)), args.positions))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fortune-telling-demo",
        description="Run deterministic demos for the bundled fortune-telling engines.",
    )
    parser.add_argument(
        "demo",
        nargs="?",
        default="all",
        choices=("all", "tarot", "astrology", "four-pillars", "nine-star-ki"),
        help="demo to run",
    )
    parser.add_argument("--json", action="store_true", help="emit serialized reading JSON")
    parser.add_argument("--seed", default=42, type=int, help="tarot RNG seed")
    parser.add_argument(
        "--positions",
        default=6,
        type=int,
        help="maximum positions to show per reading in text mode",
    )
    parser.add_argument(
        "--birth-datetime",
        default=_parse_birth_datetime(_DEFAULT_BIRTH_DATETIME),
        type=_parse_birth_datetime,
        help=(
            "birth datetime for computed traditions; naive values are interpreted "
            "in the terminal timezone"
        ),
    )
    parser.add_argument(
        "--latitude",
        default=_DEFAULT_LATITUDE,
        help="birth latitude for computed traditions",
    )
    parser.add_argument(
        "--longitude",
        default=_DEFAULT_LONGITUDE,
        help="birth longitude for computed traditions",
    )
    parser.add_argument(
        "--gender",
        default="male",
        choices=("male", "female"),
        help="Four Pillars luck-direction input",
    )
    parser.add_argument(
        "--target-year",
        default=_DEFAULT_TARGET_YEAR,
        type=int,
        help="annual year for Four Pillars and Nine Star Ki summaries",
    )
    return parser


def _selected_demos(name: str) -> tuple[_Demo, ...]:
    demos = (
        _Demo("tarot", "Tarot", _tarot_reading),
        _Demo("astrology", "Astrology", _astrology_reading),
        _Demo("four-pillars", "Four Pillars", _four_pillars_reading),
        _Demo("nine-star-ki", "Nine Star Ki", _nine_star_ki_reading),
    )
    if name == "all":
        return demos
    return tuple(demo for demo in demos if demo.key == name)


def _tarot_reading(args: argparse.Namespace) -> Reading:
    request = ReadingRequest(
        deck_id=tarot.RWS_DECK.id,
        spread_id=tarot.THREE_CARD.id,
        options={"allow_reversals": "true"},
        requested_at=_DEMO_REQUESTED_AT,
    )
    return tarot.build_engine().read(request, rng=RandomRng(seed=args.seed))


def _astrology_reading(args: argparse.Namespace) -> Reading:
    request = ReadingRequest(
        deck_id=astrology.TROPICAL_ZODIAC.id,
        spread_id=astrology.NATAL_CHART.id,
        querent=_demo_querent(args),
        requested_at=_DEMO_REQUESTED_AT,
    )
    return astrology.build_engine().cast(request)


def _four_pillars_reading(args: argparse.Namespace) -> Reading:
    request = ReadingRequest(
        deck_id=four_pillars.FOUR_PILLARS_DECK.id,
        spread_id=four_pillars.FOUR_PILLARS_SPREAD.id,
        querent=_demo_querent(args, gender=args.gender),
        options={"target_year": str(args.target_year)},
        requested_at=_DEMO_REQUESTED_AT,
    )
    return four_pillars.build_engine().cast(request)


def _nine_star_ki_reading(args: argparse.Namespace) -> Reading:
    request = ReadingRequest(
        deck_id=nine_star_ki.NINE_STAR_KI_DECK.id,
        spread_id=nine_star_ki.NINE_STAR_KI_SPREAD.id,
        querent=_demo_querent(args),
        options={"target_year": str(args.target_year)},
        requested_at=_DEMO_REQUESTED_AT,
    )
    return nine_star_ki.build_engine(target_year=args.target_year).cast(request)


def _demo_querent(args: argparse.Namespace, *, gender: str | None = None) -> Querent:
    attributes = {
        "birth_datetime": str(args.birth_datetime),
        "latitude": str(args.latitude),
        "longitude": str(args.longitude),
    }
    if gender is not None:
        attributes["gender"] = gender
    return Querent(id="demo", display_name="Demo Querent", attributes=attributes)


def _parse_birth_datetime(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("birth datetime must be an ISO-8601 datetime") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        parsed = parsed.astimezone()
    return parsed.isoformat()


def _render_readings(items: tuple[tuple[_Demo, Reading], ...], max_positions: int) -> str:
    parts: list[str] = []
    for demo, reading in items:
        parts.append("\n".join(_render_reading(demo, reading, max_positions)))
    return "\n\n".join(parts)


def _render_reading(demo: _Demo, reading: Reading, max_positions: int) -> list[str]:
    lines = [
        f"{demo.title}",
        f"Engine: {reading.provenance.engine_id}@{reading.provenance.engine_version}",
        f"Deck: {reading.provenance.deck_id}",
        f"Spread: {reading.spread.name} ({reading.spread.id})",
        f"Replay artifact: {len(reading.draw.selections)} recorded selections",
        "Positions:",
    ]
    shown_positions = reading.positions[: max(max_positions, 0)]
    for position in shown_positions:
        modifier_text = _format_modifiers(position.selection.modifiers)
        lines.append(
            f"- {position.position.name}: {position.symbol.name}"
            f"{modifier_text} [{position.symbol.id}]"
        )
    if len(reading.positions) > len(shown_positions):
        lines.append(f"- ... {len(reading.positions) - len(shown_positions)} more positions")
    if reading.summary:
        lines.append(f"Summary: {reading.summary}")
    notes = ", ".join(reading.provenance.notes)
    if notes:
        lines.append(f"Provenance notes: {notes}")
    return lines


def _format_modifiers(modifiers: object) -> str:
    if not isinstance(modifiers, dict) or not modifiers:
        return ""
    interesting = (
        "orientation",
        "longitude",
        "house",
        "retrograde",
        "cjk",
        "element",
        "polarity",
        "ten_god",
        "role",
    )
    parts = [f"{key}={modifiers[key]}" for key in interesting if key in modifiers]
    return "" if not parts else f" ({', '.join(parts)})"


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
