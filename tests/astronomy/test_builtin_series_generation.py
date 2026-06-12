from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


def test_builtin_series_matches_source_tables() -> None:
    root = Path(__file__).resolve().parents[2]
    _skip_if_vsop87d_cache_is_missing(root)

    result = subprocess.run(
        [sys.executable, "tools/ephemeris/generate_builtin_series.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def _skip_if_vsop87d_cache_is_missing(root: Path) -> None:
    source_root = root / "tools/ephemeris/sources"
    vsop87d_root = root / ".cache/ephemeris/vsop87d"
    manifest = source_root / "MANIFEST.sha256"
    missing = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        _checksum, relative_path = stripped.split(maxsplit=1)
        if relative_path.startswith("vsop87d/"):
            path = vsop87d_root / Path(relative_path).name
            if not path.exists():
                missing.append(relative_path)

    if missing:
        pytest.skip(
            "VSOP87D source cache is not populated; run "
            "`python tools/ephemeris/download_vsop87d.py` to enable this check"
        )
