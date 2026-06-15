"""Parsers for user-supplied, third-party stroke-count datasets.

These convert a stroke-count dataset that *you* obtain and supply into a
``{character: stroke_count}`` mapping suitable for the ``cjk_name_strokes``
engine's ``provider`` (or ``request``) stroke source. No third-party data is
bundled — the datasets below are under share-alike licences (CC BY-SA), whose
ShareAlike terms are incompatible with bundling them in this project, so the
caller is responsible for downloading them and complying with their terms.

Supported formats:

- :func:`parse_kanjidic2` — EDRDG KANJIDIC2 XML (CC BY-SA 4.0,
  https://www.edrdg.org/wiki/index.php/KANJIDIC_Project). Modern Japanese
  (shinjitai) stroke counts.
- :func:`parse_kanjivg` — KanjiVG SVG / aggregated XML (CC BY-SA 3.0,
  https://kanjivg.tagaini.net/). Stroke counts derived by counting stroke
  paths, again on modern Japanese glyphs.

Both produce literal, as-printed counts without radical restoration; like the
bundled Unihan source they are not faithful to Kangxi-based ``seimei handan``
schools. Wrap the parsed mapping in a
:class:`fortune_telling_core.traditions.cjk_name_strokes.providers.MappingStrokeProvider`
and register it to use it as a ``stroke_source``.

Example:
    ```python
    from fortune_telling_core import ReadingRequest
    from fortune_telling_core.traditions.cjk_name_strokes import (
        CJK_NAME_STROKES_DECK,
        CJK_NAME_STROKES_SPREAD,
        MappingStrokeProvider,
        build_engine,
        parse_kanjidic2,
        register_provider,
    )

    # You download kanjidic2.xml yourself (CC BY-SA 4.0) and comply with its terms.
    with open("kanjidic2.xml", "rb") as fh:
        table = parse_kanjidic2(fh)
    register_provider(MappingStrokeProvider("kanjidic2", "2024-01", table))

    request = ReadingRequest(
        deck_id=CJK_NAME_STROKES_DECK.id,
        spread_id=CJK_NAME_STROKES_SPREAD.id,
        options={"surname": "山田", "given_name": "太郎", "stroke_source": "kanjidic2"},
    )
    reading = build_engine().cast(request)
    ```
"""

from __future__ import annotations

import re
from typing import IO
from xml.etree.ElementTree import iterparse

from fortune_telling_core.errors import ValidationError

_Source = str | IO[bytes]
_KVG_ROOT_ID = re.compile(r"kvg:([0-9a-fA-F]{4,6})$")


def _local(tag: str) -> str:
    """Return an XML tag's local name, dropping any ``{namespace}`` prefix."""

    return tag.rsplit("}", 1)[-1]


def parse_kanjidic2(source: _Source) -> dict[str, int]:
    """Parse total stroke counts from an EDRDG KANJIDIC2 XML file.

    Each ``<character>`` carries its glyph in ``<literal>`` and one or more
    ``<misc><stroke_count>`` values. Per the KANJIDIC2 DTD, the first
    ``stroke_count`` is the accepted count and any others are common miscounts,
    so only the first is used.

    Args:
        source: A path to the KANJIDIC2 XML file, or a binary file object.

    Returns:
        A mapping of each character to its accepted total stroke count.

    Raises:
        ValidationError: If a ``<character>`` has a literal but no stroke count.
    """

    table: dict[str, int] = {}
    for _event, element in iterparse(source, events=("end",)):
        if _local(element.tag) != "character":
            continue
        literal: str | None = None
        strokes: int | None = None
        for child in element:
            name = _local(child.tag)
            if name == "literal":
                literal = (child.text or "").strip() or None
            elif name == "misc":
                for grandchild in child:
                    if _local(grandchild.tag) == "stroke_count":
                        strokes = int((grandchild.text or "").strip())
                        break
        element.clear()
        if literal is None:
            continue
        if strokes is None:
            raise ValidationError(f"KANJIDIC2 character {literal!r} has no stroke_count")
        table[literal] = strokes
    return table


def parse_kanjivg(source: _Source) -> dict[str, int]:
    """Parse stroke counts from KanjiVG SVG or aggregated XML data.

    Each kanji's strokes live under a group whose ``id`` is ``kvg:<hex>`` (the
    bare codepoint, without the ``StrokePaths_``/``kanji_`` wrappers or the
    ``-g``/``-s`` component suffixes). The stroke count is the number of
    ``<path>`` elements in that group; the ``<text>`` stroke-number annotations
    live in a separate group and are not counted. This works for both a single
    ``<svg>`` file and the aggregated ``kanjivg-*.xml`` release.

    Args:
        source: A path to a KanjiVG SVG / XML file, or a binary file object.

    Returns:
        A mapping of each character to its stroke count.
    """

    table: dict[str, int] = {}
    for _event, element in iterparse(source, events=("end",)):
        if _local(element.tag) != "g":
            continue
        match = _KVG_ROOT_ID.fullmatch(element.get("id", ""))
        if match is None:
            continue
        char = chr(int(match.group(1), 16))
        table[char] = sum(1 for node in element.iter() if _local(node.tag) == "path")
        element.clear()
    return table
