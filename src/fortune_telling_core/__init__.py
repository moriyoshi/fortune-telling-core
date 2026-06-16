from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""Core primitives for composable fortune-telling systems.

The top-level package exports only tradition-agnostic value objects, engine
protocols, RNG helpers, errors, and reading serialization functions. Tradition
engines are available from their own subpackages.

Example:
    ```python
    from fortune_telling_core import ReadingRequest

    request = ReadingRequest(
        deck_id="example.deck",
        spread_id="example.spread",
    )
    ```
"""

try:
    # Single source of truth: _version.py is generated from the git tag by
    # hatch-vcs at build/install time (see pyproject [tool.hatch.build.hooks.vcs]).
    from fortune_telling_core._version import __version__  # noqa: E402
except ImportError:  # pragma: no cover - generated file absent in an unbuilt tree
    __version__ = "0.0.0+unknown"

from fortune_telling_core.draw import Draw, Selection  # noqa: E402
from fortune_telling_core.engine import Engine  # noqa: E402
from fortune_telling_core.errors import (  # noqa: E402
    ExhaustedRngError,
    FortuneTellingError,
    SchemaVersionError,
    UnknownSymbolError,
    ValidationError,
)
from fortune_telling_core.provenance import Provenance  # noqa: E402
from fortune_telling_core.reading import PositionReading, Reading  # noqa: E402
from fortune_telling_core.request import Querent, ReadingRequest  # noqa: E402
from fortune_telling_core.rng import RandomRng, Rng, SequenceRng  # noqa: E402
from fortune_telling_core.serde import (  # noqa: E402
    SCHEMA_VERSION,
    reading_from_json,
    reading_to_json,
)
from fortune_telling_core.spread import Position, Spread  # noqa: E402
from fortune_telling_core.symbols import Deck, Symbol  # noqa: E402

__all__ = [
    "SCHEMA_VERSION",
    "Deck",
    "Draw",
    "Engine",
    "ExhaustedRngError",
    "FortuneTellingError",
    "Position",
    "PositionReading",
    "Provenance",
    "Querent",
    "RandomRng",
    "Reading",
    "ReadingRequest",
    "Rng",
    "SchemaVersionError",
    "Selection",
    "SequenceRng",
    "Spread",
    "Symbol",
    "UnknownSymbolError",
    "ValidationError",
    "__version__",
    "reading_from_json",
    "reading_to_json",
]
