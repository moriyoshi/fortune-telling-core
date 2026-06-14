"""Generate the bundled Unihan total-stroke table from the Unihan archive.

Extracts the ``kTotalStrokes`` property from ``Unihan_IRGSources.txt`` inside
the cached Unihan archive and writes the packed, gzipped lookup table to
``src/fortune_telling_core/traditions/_name_values/data/unihan_total_strokes.bin.gz``
(delta-varint code points plus a stroke byte each; see ``cjk_unihan_strokes``).

Per Unicode UAX #38 a ``kTotalStrokes`` entry may carry two space-separated
values; the first is the canonical count for the most customary form and is the
one bundled here.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from download_unihan import UNIHAN_CACHE, download_missing_unihan

from fortune_telling_core.traditions._name_values.cjk_unihan_strokes import encode_table

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = UNIHAN_CACHE / "Unihan-15.0.0.zip"
ARCHIVE_MEMBER = "Unihan_IRGSources.txt"
UNICODE_VERSION = "15.0.0"
OUTPUT = ROOT / "src/fortune_telling_core/traditions/_name_values/data/unihan_total_strokes.bin.gz"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download-missing",
        action="store_true",
        help="download the Unihan archive into the local cache if absent",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed table matches the source instead of writing it",
    )
    args = parser.parse_args()

    if args.download_missing:
        download_missing_unihan()

    rendered = encode_table(_read_total_strokes())

    if args.check:
        current = OUTPUT.read_bytes() if OUTPUT.exists() else b""
        if current != rendered:
            raise SystemExit(
                f"{OUTPUT} is out of date; rerun tools/unihan/generate_total_strokes.py"
            )
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(rendered)
    return 0


def _read_total_strokes() -> dict[int, int]:
    if not ARCHIVE.exists():
        raise SystemExit(
            f"missing {ARCHIVE}; run with --download-missing or "
            "python tools/unihan/download_unihan.py"
        )
    counts: dict[int, int] = {}
    with zipfile.ZipFile(ARCHIVE) as archive:
        payload = archive.read(ARCHIVE_MEMBER).decode("utf-8")
    for line in payload.splitlines():
        if not line or line.startswith("#"):
            continue
        codepoint, field, value = line.split("\t", 2)
        if field != "kTotalStrokes":
            continue
        counts[int(codepoint[2:], 16)] = int(value.split(" ", 1)[0])
    return counts


if __name__ == "__main__":
    raise SystemExit(main())
