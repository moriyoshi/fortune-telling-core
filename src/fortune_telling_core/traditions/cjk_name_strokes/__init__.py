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
    build_engine,
)
from fortune_telling_core.traditions.cjk_name_strokes.parsers import (  # noqa: E402
    parse_kanjidic2,
    parse_kanjivg,
)
from fortune_telling_core.traditions.cjk_name_strokes.providers import (  # noqa: E402
    DEFAULT_PROVIDER,
    MappingStrokeProvider,
    StrokeCountProvider,
    StrokeProviderRegistry,
    default_registry,
    new_default_registry,
    register_provider,
)
from fortune_telling_core.traditions.cjk_name_strokes.spreads import (  # noqa: E402
    CJK_NAME_STROKES_SPREAD,
)

__all__ = [
    "CJK_NAME_STROKES_DECK",
    "CJK_NAME_STROKES_SPREAD",
    "DEFAULT_PROVIDER",
    "CharacterSet",
    "CjkNameStrokesEngine",
    "Grid",
    "MappingStrokeProvider",
    "School",
    "StrokeCountProvider",
    "StrokeProviderRegistry",
    "build_engine",
    "default_registry",
    "new_default_registry",
    "parse_kanjidic2",
    "parse_kanjivg",
    "register_provider",
]
