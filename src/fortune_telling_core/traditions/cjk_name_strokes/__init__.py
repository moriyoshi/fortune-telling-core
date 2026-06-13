from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
"""CJK name stroke onomancy tradition implementation."""

from fortune_telling_core.traditions.cjk_name_strokes.deck import (  # noqa: E402
    CJK_NAME_STROKES_DECK,
)
from fortune_telling_core.traditions.cjk_name_strokes.engine import (  # noqa: E402
    CharacterSet,
    CjkNameStrokesEngine,
    Grid,
    School,
    StrokeSource,
    build_engine,
)
from fortune_telling_core.traditions.cjk_name_strokes.spreads import (  # noqa: E402
    CJK_NAME_STROKES_SPREAD,
)

__all__ = [
    "CJK_NAME_STROKES_DECK",
    "CJK_NAME_STROKES_SPREAD",
    "CharacterSet",
    "CjkNameStrokesEngine",
    "Grid",
    "School",
    "StrokeSource",
    "build_engine",
]
