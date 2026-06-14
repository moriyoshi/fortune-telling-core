"""Stroke-count providers and a registry for the CJK name-stroke engine.

A :class:`StrokeCountProvider` resolves a character to a total stroke count under
an explicit, named source. The engine selects a provider by name via the
``stroke_source`` option (default ``"unihan"``). The bundled Unicode Unihan
``kTotalStrokes`` table is registered as ``"unihan"``; a caller can register its
own providers — for example wrapping a third-party dataset parsed by
:mod:`fortune_telling_core.traditions.cjk_name_strokes.parsers` — with
:func:`register_provider` (the process-wide default registry) or against a
private :class:`StrokeProviderRegistry` passed to ``build_engine``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_values import cjk_unihan_strokes

DEFAULT_PROVIDER = "unihan"


@runtime_checkable
class StrokeCountProvider(Protocol):
    """Resolves CJK characters to total stroke counts under a named source.

    Implementations expose a stable ``id`` and ``version`` (recorded as the
    reading's value system) and resolve single characters to counts.
    """

    @property
    def id(self) -> str:
        """Stable identifier recorded as the reading's value system."""

    @property
    def version(self) -> str:
        """Value-system version recorded on the reading."""

    def stroke_count(self, char: str) -> int | None:
        """Return the total stroke count for ``char``, or ``None`` if unknown."""


@dataclass(frozen=True, slots=True)
class MappingStrokeProvider:
    """A provider backed by an in-memory ``{character: stroke_count}`` mapping.

    Wrap a dataset parsed by
    :func:`fortune_telling_core.traditions.cjk_name_strokes.parsers.parse_kanjidic2`
    / ``parse_kanjivg`` (or your own school table) and register it; ``id`` and
    ``version`` identify the dataset in provenance.
    """

    id: str
    version: str
    mapping: Mapping[str, int]

    def stroke_count(self, char: str) -> int | None:
        return self.mapping.get(char)


class _UnihanStrokeProvider:
    """The bundled Unicode Unihan ``kTotalStrokes`` provider."""

    id = cjk_unihan_strokes.ID
    version = cjk_unihan_strokes.VERSION

    def stroke_count(self, char: str) -> int | None:
        return cjk_unihan_strokes.stroke_count(char)


class StrokeProviderRegistry:
    """A name to :class:`StrokeCountProvider` registry."""

    def __init__(self) -> None:
        self._providers: dict[str, StrokeCountProvider] = {}

    def register(self, provider: StrokeCountProvider, *, name: str | None = None) -> str:
        """Register ``provider`` under ``name`` (defaults to ``provider.id``).

        Args:
            provider: The provider to register.
            name: The lookup name; defaults to the provider's ``id``.

        Returns:
            The name the provider was registered under.

        Raises:
            ValidationError: If the resolved name is empty.
        """

        key = name if name is not None else provider.id
        if not key:
            raise ValidationError("stroke provider name must not be empty")
        self._providers[key] = provider
        return key

    def get(self, name: str) -> StrokeCountProvider:
        """Return the provider registered under ``name``.

        Raises:
            ValidationError: If no provider is registered under ``name``.
        """

        provider = self._providers.get(name)
        if provider is None:
            available = ", ".join(self.names()) or "(none)"
            raise ValidationError(f"unknown stroke provider: {name!r} (registered: {available})")
        return provider

    def names(self) -> tuple[str, ...]:
        """Return the registered provider names, sorted."""

        return tuple(sorted(self._providers))


def new_default_registry() -> StrokeProviderRegistry:
    """Return a fresh registry seeded with only the bundled ``unihan`` provider."""

    registry = StrokeProviderRegistry()
    registry.register(_UnihanStrokeProvider(), name=DEFAULT_PROVIDER)
    return registry


_DEFAULT_REGISTRY = new_default_registry()


def default_registry() -> StrokeProviderRegistry:
    """Return the process-wide default stroke-provider registry."""

    return _DEFAULT_REGISTRY


def register_provider(provider: StrokeCountProvider, *, name: str | None = None) -> str:
    """Register ``provider`` in the process-wide default registry.

    Args:
        provider: The provider to register.
        name: The lookup name; defaults to the provider's ``id``.

    Returns:
        The name the provider was registered under (use it as ``stroke_source``).
    """

    return _DEFAULT_REGISTRY.register(provider, name=name)
