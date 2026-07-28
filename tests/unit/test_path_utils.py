"""Tests for path utility functions."""

from nautilus_developer_toolkit.utils.paths import get_local_path, module_name_from_file


def test_module_name_from_file() -> None:
    result = module_name_from_file(
        "/tmp/project",
        "/tmp/project/src/api/main.py",
    )

    assert result == "src.api.main"


class FakeLocation:
    def __init__(self, path: str | None) -> None:
        self.path = path

    def get_path(self) -> str | None:
        return self.path


class FakeFileInfo:
    def __init__(self, location: FakeLocation | None) -> None:
        self.location = location

    def get_location(self) -> FakeLocation | None:
        return self.location


def test_get_local_path_returns_unchanged_local_path() -> None:
    assert (
        get_local_path(FakeFileInfo(FakeLocation("/tmp/project with spaces")))
        == "/tmp/project with spaces"
    )


def test_get_local_path_returns_none_without_location() -> None:
    assert get_local_path(FakeFileInfo(None)) is None


def test_get_local_path_preserves_none_path() -> None:
    assert get_local_path(FakeFileInfo(FakeLocation(None))) is None


def test_get_local_path_preserves_missing_get_location_error() -> None:
    class MissingLocation:
        pass

    try:
        get_local_path(MissingLocation())
    except AttributeError:
        pass
    else:
        raise AssertionError("Expected AttributeError")
