"""CJK name stroke onomancy engine."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum

from fortune_telling_core._null_rng import NullRng
from fortune_telling_core._parsing import collect_values, require_string
from fortune_telling_core.draw import Draw, Selection
from fortune_telling_core.engine import AbstractEngine
from fortune_telling_core.errors import ValidationError
from fortune_telling_core.reading import Reading
from fortune_telling_core.request import ReadingRequest
from fortune_telling_core.rng import Rng
from fortune_telling_core.spread import Spread
from fortune_telling_core.symbols import Deck
from fortune_telling_core.traditions._name_text import NameValueUnit, format_value_trace
from fortune_telling_core.traditions.cjk_name_strokes.deck import (
    CJK_NAME_STROKES_DECK,
    GRID_SYMBOLS,
)
from fortune_telling_core.traditions.cjk_name_strokes.providers import (
    DEFAULT_PROVIDER,
    StrokeCountProvider,
    StrokeProviderRegistry,
    default_registry,
)
from fortune_telling_core.traditions.cjk_name_strokes.spreads import CJK_NAME_STROKES_SPREAD

_NULL_RNG = NullRng("CjkNameStrokesEngine.cast must not use randomness")


class School(StrEnum):
    """Supported CJK name stroke schools."""

    JAPANESE_SEIMEI_HANDAN = "japanese_seimei_handan"
    CHINESE_XINGMINGXUE = "chinese_xingmingxue"


class CharacterSet(StrEnum):
    """Declared character-set basis for request-supplied counts."""

    TRADITIONAL = "traditional"
    SIMPLIFIED = "simplified"
    SHINJITAI = "shinjitai"
    KYUJITAI = "kyujitai"


class Grid(StrEnum):
    """Supported stroke grids."""

    FIVE_GRID = "five_grid"


@dataclass(frozen=True, slots=True)
class StrokeChart:
    """Resolved CJK five-grid stroke values."""

    surname: str
    given_name: str
    units: tuple[NameValueUnit, ...]
    heaven: int
    person: int
    earth: int
    outer: int
    total: int


class CjkNameStrokesEngine(AbstractEngine):
    """CJK name stroke onomancy engine.

    Stroke counts are resolved by a named :class:`StrokeCountProvider` selected
    via the ``stroke_source`` option (default ``"unihan"``, the bundled Unihan
    table). Providers are looked up in ``registry`` — the process-wide default
    registry unless one is injected.
    """

    id = "cjk_name_strokes.engine"
    version = "0.1.0"

    def __init__(self, *, registry: StrokeProviderRegistry | None = None) -> None:
        self._registry = registry if registry is not None else default_registry()

    def deck(self, request: ReadingRequest) -> Deck:
        """Return the CJK name strokes deck."""

        if request.deck_id != CJK_NAME_STROKES_DECK.id:
            raise ValidationError(f"unsupported CJK name strokes deck: {request.deck_id}")
        return CJK_NAME_STROKES_DECK

    def spread(self, request: ReadingRequest) -> Spread:
        """Return the CJK name strokes spread."""

        if request.spread_id != CJK_NAME_STROKES_SPREAD.id:
            raise ValidationError(f"unsupported CJK name strokes spread: {request.spread_id}")
        return CJK_NAME_STROKES_SPREAD

    def draw(self, request: ReadingRequest, rng: Rng) -> Draw:
        """Compute the CJK five-grid stroke chart as a deterministic draw."""

        del rng
        fields = collect_values(request)
        surname = require_string(fields, "surname")
        given_name = require_string(fields, "given_name")
        school = _parse(fields.get("school"), School.JAPANESE_SEIMEI_HANDAN)
        character_set = _parse(fields.get("character_set"), CharacterSet.SHINJITAI)
        grid = _parse(fields.get("grid"), Grid.FIVE_GRID)
        provider_name = fields.get("stroke_source") or DEFAULT_PROVIDER
        provider = self._registry.get(provider_name)
        strokes = _resolve_strokes(surname, given_name, provider, provider_name)
        chart = _compute_chart(surname, given_name, strokes)

        common = {
            "value_system": provider.id,
            "value_system_version": provider.version,
            "school": school.value,
            "character_set": character_set.value,
            "stroke_source": provider_name,
            "grid": grid.value,
        }
        trace = {
            **common,
            "surname": chart.surname,
            "given_name": chart.given_name,
            "characters": "".join(unit.char for unit in chart.units),
            "values": format_value_trace(chart.units),
        }
        selections = (
            _grid_selection("heaven", chart.heaven, common),
            _grid_selection("person", chart.person, common),
            _grid_selection("earth", chart.earth, common),
            _grid_selection("outer", chart.outer, common),
            Selection(
                "total",
                GRID_SYMBOLS["total"],
                {
                    **trace,
                    "value": str(chart.total),
                    "total": str(chart.total),
                    "heaven": str(chart.heaven),
                    "person": str(chart.person),
                    "earth": str(chart.earth),
                    "outer": str(chart.outer),
                },
            ),
        )
        return Draw(CJK_NAME_STROKES_DECK.id, CJK_NAME_STROKES_SPREAD.id, selections)

    def cast(self, request: ReadingRequest) -> Reading:
        """Compute a CJK name stroke reading without a caller RNG."""

        draw = self.draw(request, _NULL_RNG)
        return self._interpret(request, draw, rng=None)

    def _interpret(self, request: ReadingRequest, draw: Draw, rng: Rng | None) -> Reading:
        base = super()._interpret(request, draw, rng)
        total = dict(draw.selections[-1].modifiers or {})
        summary = (
            f"CJK name stroke total {total['total']}; heaven {total['heaven']}; "
            f"person {total['person']}; earth {total['earth']}; outer {total['outer']}."
        )
        notes = tuple(base.provenance.notes) + (
            "system=cjk_name_strokes",
            f"value_system={total['value_system']}",
            f"school={total['school']}",
            f"character_set={total['character_set']}",
            f"stroke_source={total['stroke_source']}",
            f"grid={total['grid']}",
        )
        return replace(
            base,
            summary=summary,
            provenance=replace(base.provenance, notes=notes, rng_kind=None, rng_seed=None),
        )


def _resolve_strokes(
    surname: str,
    given_name: str,
    provider: StrokeCountProvider,
    provider_name: str,
) -> dict[str, int]:
    strokes: dict[str, int] = {}
    for char in surname + given_name:
        count = provider.stroke_count(char)
        if count is None:
            raise ValidationError(
                f"stroke provider {provider_name!r} has no count for {char!r} (U+{ord(char):04X})"
            )
        strokes[char] = count
    return strokes


def _grid_selection(position_id: str, value: int, common: dict[str, str]) -> Selection:
    return Selection(
        position_id,
        GRID_SYMBOLS[position_id],
        {
            **common,
            "value": str(value),
            "trace_position": "total",
        },
    )


def _compute_chart(surname: str, given_name: str, strokes: dict[str, int]) -> StrokeChart:
    if not surname:
        raise ValidationError("surname must not be empty")
    if not given_name:
        raise ValidationError("given_name must not be empty")

    name = surname + given_name
    units: list[NameValueUnit] = []
    for char in name:
        value = strokes.get(char)
        if value is None:
            raise ValidationError(f"missing stroke count for character: {char!r}")
        if value <= 0:
            raise ValidationError(f"stroke count must be positive for character: {char!r}")
        units.append(NameValueUnit(char, value))

    surname_values = [unit.value for unit in units[: len(surname)]]
    given_values = [unit.value for unit in units[len(surname) :]]
    virtual_surname = 1 if len(surname_values) == 1 else 0
    virtual_given = 1 if len(given_values) == 1 else 0
    heaven = sum(surname_values) + virtual_surname
    person = surname_values[-1] + given_values[0]
    earth = sum(given_values) + virtual_given
    total = sum(unit.value for unit in units)
    outer = total - person + virtual_surname + virtual_given
    return StrokeChart(
        surname=surname,
        given_name=given_name,
        units=tuple(units),
        heaven=heaven,
        person=person,
        earth=earth,
        outer=outer,
        total=total,
    )


def _parse[T: StrEnum](value: str | None, default: T) -> T:
    if value is None or value == "":
        return default
    try:
        return type(default)(value)
    except ValueError as exc:
        raise ValidationError(f"unsupported {type(default).__name__}: {value!r}") from exc


def build_engine(*, registry: StrokeProviderRegistry | None = None) -> CjkNameStrokesEngine:
    """Create a CJK name stroke onomancy engine.

    Args:
        registry: Stroke-provider registry to resolve ``stroke_source`` against;
            defaults to the process-wide registry.
    """

    return CjkNameStrokesEngine(registry=registry)
