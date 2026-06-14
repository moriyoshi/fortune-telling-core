"""CJK total-stroke value system backed by the Unicode Unihan database.

Resolves CJK ideographs to their ``kTotalStrokes`` count from a bundled table
generated from the Unihan database (see ``tools/unihan/``). These are
representative-glyph totals per Unicode UAX #38, not the Kangxi or school-
specific counts that a given ``seimei handan`` or ``xingmingxue`` school may
require; engines using this system should record that caveat in provenance.

The table ships as a packed, gzipped binary (``unihan_total_strokes.bin.gz``):
the sorted code points are delta-varint encoded and each carries a one-byte
stroke count, which compresses to a fraction of the equivalent text table. It is
decoded lazily on first use and cached for the process lifetime. See
``data/UNIHAN-NOTICE.txt`` for source and license, and
``tools/unihan/generate_total_strokes.py`` for regeneration.
"""

from __future__ import annotations

import gzip
import importlib.resources
from collections.abc import Mapping

from fortune_telling_core.errors import ValidationError
from fortune_telling_core.traditions._name_text import NameValueUnit

ID = "cjk_unihan_strokes.v1"
VERSION = "15.0.0"

_DATA_PACKAGE = "fortune_telling_core.traditions._name_values"
_DATA_RESOURCE = ("data", "unihan_total_strokes.bin.gz")

# Packed-table format: b"UTS1" magic, uint32-LE entry count, then the count
# code points as ULEB128 deltas of the sorted code points, then one stroke byte
# per entry in the same order. The whole payload is gzip-compressed.
_MAGIC = b"UTS1"

_TABLE: dict[str, int] | None = None


def encode_table(counts: Mapping[int, int]) -> bytes:
    """Pack a ``{codepoint: stroke_count}`` table into the gzipped binary form.

    Args:
        counts: Map of Unicode code point to total stroke count.

    Returns:
        The gzip-compressed packed table (deterministic for a given input).

    Raises:
        ValueError: If a stroke count does not fit in a single byte.
    """

    items = sorted(counts.items())
    deltas = bytearray()
    strokes = bytearray()
    previous = 0
    for codepoint, count in items:
        if not 0 <= count <= 0xFF:
            raise ValueError(f"stroke count out of byte range: {count}")
        delta = codepoint - previous
        previous = codepoint
        while True:
            byte = delta & 0x7F
            delta >>= 7
            deltas.append(byte | (0x80 if delta else 0))
            if not delta:
                break
        strokes.append(count)
    payload = _MAGIC + len(items).to_bytes(4, "little") + bytes(deltas) + bytes(strokes)
    return gzip.compress(payload, compresslevel=9, mtime=0)


def decode_table(blob: bytes) -> dict[str, int]:
    """Decode a gzipped packed table back into ``{char: stroke_count}``.

    Args:
        blob: The gzip-compressed packed table from :func:`encode_table`.

    Returns:
        Map of character to total stroke count.

    Raises:
        ValidationError: If the payload is malformed or truncated.
    """

    payload = gzip.decompress(blob)
    if payload[:4] != _MAGIC:
        raise ValidationError("unihan stroke table has an unexpected format")
    count = int.from_bytes(payload[4:8], "little")
    pos = 8
    end = len(payload) - count
    if end < pos:
        raise ValidationError("unihan stroke table is truncated")
    table: dict[str, int] = {}
    codepoint = 0
    for index in range(count):
        delta = 0
        shift = 0
        while True:
            if pos >= end:
                raise ValidationError("unihan stroke table is truncated")
            byte = payload[pos]
            pos += 1
            delta |= (byte & 0x7F) << shift
            if not byte & 0x80:
                break
            shift += 7
        codepoint += delta
        table[chr(codepoint)] = payload[end + index]
    if pos != end:
        raise ValidationError("unihan stroke table has trailing data")
    return table


def _table() -> dict[str, int]:
    global _TABLE
    if _TABLE is None:
        resource = importlib.resources.files(_DATA_PACKAGE).joinpath(*_DATA_RESOURCE)
        _TABLE = decode_table(resource.read_bytes())
    return _TABLE


def stroke_count(char: str) -> int | None:
    """Return the Unihan total stroke count for ``char``, or ``None`` if absent."""

    return _table().get(char)


def values(name: str) -> tuple[NameValueUnit, ...]:
    """Return the per-character Unihan stroke values for ``name``.

    Args:
        name: The CJK name or name part to evaluate.

    Returns:
        One :class:`NameValueUnit` per character, in input order.

    Raises:
        ValidationError: If a character has no Unihan ``kTotalStrokes`` entry.
    """

    table = _table()
    units: list[NameValueUnit] = []
    for char in name:
        count = table.get(char)
        if count is None:
            raise ValidationError(
                f"no Unihan stroke count for character: {char!r} (U+{ord(char):04X})"
            )
        units.append(NameValueUnit(char, count))
    return tuple(units)
