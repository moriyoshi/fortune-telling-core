"""Download VSOP87D source tables used by the built-in ephemeris generator."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path(__file__).resolve().parent / "sources"
VSOP87D_ROOT = ROOT / ".cache/ephemeris/vsop87d"
MANIFEST = SOURCE_ROOT / "MANIFEST.sha256"
VSOP87D_BASE_URL = "https://ftp.imcce.fr/pub/ephem/planets/vsop87/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="redownload files even when local checksums already match",
    )
    args = parser.parse_args()

    download_missing_vsop87d(force=args.force)
    return 0


def download_missing_vsop87d(*, force: bool = False) -> None:
    """Populate the local VSOP87D cache and verify each downloaded file."""
    VSOP87D_ROOT.mkdir(parents=True, exist_ok=True)
    for relative_path, expected_hash in _read_vsop87d_manifest().items():
        path = VSOP87D_ROOT / Path(relative_path).name
        if not force and path.exists() and _sha256(path.read_bytes()) == expected_hash:
            continue

        url = VSOP87D_BASE_URL + path.name
        payload = _download(url)
        actual_hash = _sha256(payload)
        if actual_hash != expected_hash:
            raise SystemExit(
                f"checksum mismatch for {url}: expected {expected_hash}, got {actual_hash}"
            )
        path.write_bytes(payload)


def _read_vsop87d_manifest() -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        checksum, relative_path = stripped.split(maxsplit=1)
        if relative_path.startswith("vsop87d/"):
            checksums[relative_path] = checksum
    return checksums


def _download(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:
        return response.read()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
