from importlib.metadata import version

from fortune_telling_core import __version__


def test_package_version_tracks_vcs_metadata() -> None:
    # __version__ must stay synchronized with the hatch-vcs-derived distribution
    # metadata (the git tag), not a hardcoded literal that drifts.
    assert __version__ == version("fortune-telling-core")
