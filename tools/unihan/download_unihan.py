"""Download the Unihan database archive used by the stroke-count generator."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(__file__).resolve().parent / "sources"
UNIHAN_CACHE = ROOT / ".cache/unihan"
MANIFEST = SOURCE_ROOT / "MANIFEST.sha256"
UNIHAN_BASE_URL = "https://www.unicode.org/Public/15.0.0/ucd/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="redownload archives even when local checksums already match",
    )
    args = parser.parse_args()

    download_missing_unihan(force=args.force)
    return 0


def download_missing_unihan(*, force: bool = False) -> None:
    """Populate the local Unihan cache and verify each downloaded archive."""
    UNIHAN_CACHE.mkdir(parents=True, exist_ok=True)
    for relative_path, expected_hash in _read_manifest().items():
        path = UNIHAN_CACHE / Path(relative_path).name
        if not force and path.exists() and _sha256(path.read_bytes()) == expected_hash:
            continue

        url = UNIHAN_BASE_URL + "Unihan.zip"
        payload = _download(url)
        actual_hash = _sha256(payload)
        if actual_hash != expected_hash:
            raise SystemExit(
                f"checksum mismatch for {url}: expected {expected_hash}, got {actual_hash}"
            )
        path.write_bytes(payload)


def _read_manifest() -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        checksum, relative_path = stripped.split(maxsplit=1)
        if relative_path.startswith("unihan/"):
            checksums[relative_path] = checksum
    return checksums


def _download(url: str) -> bytes:
    with urlopen(url, timeout=60) as response:
        data: bytes = response.read()
        return data


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
