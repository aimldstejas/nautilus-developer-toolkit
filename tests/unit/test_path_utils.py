"""Tests for path utility functions."""

from nautilus_developer_toolkit.utils.paths import module_name_from_file


def test_module_name_from_file() -> None:
    result = module_name_from_file(
        "/tmp/project",
        "/tmp/project/src/api/main.py",
    )

    assert result == "src.api.main"
