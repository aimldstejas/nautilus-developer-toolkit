"""Tests for filesystem utility functions."""

from pathlib import Path

import pytest

from nautilus_developer_toolkit.utils.filesystem import (
    file_contains_any,
    find_python_files,
    search_upwards,
    write_new_file,
)


def test_search_upwards_finds_marker(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    nested = project_root / "src" / "package"
    nested.mkdir(parents=True)

    marker = project_root / "pyproject.toml"
    marker.write_text("[project]\n", encoding="utf-8")

    result = search_upwards(str(nested), ["pyproject.toml"])

    assert result == marker


def test_search_upwards_returns_none_when_missing(tmp_path: Path) -> None:
    nested = tmp_path / "project" / "src"
    nested.mkdir(parents=True)

    result = search_upwards(str(nested), ["missing.marker"])

    assert result is None


def test_file_contains_any_matches_case_insensitively(tmp_path: Path) -> None:
    file_path = tmp_path / "app.py"
    file_path.write_text("from FastAPI import FastAPI\n", encoding="utf-8")

    assert file_contains_any(file_path, ["fastapi"])


def test_file_contains_any_returns_false_for_missing_file(tmp_path: Path) -> None:
    assert not file_contains_any(tmp_path / "missing.txt", ["python"])


def test_find_python_files_skips_excluded_directories(tmp_path: Path) -> None:
    included = tmp_path / "src" / "app.py"
    excluded = tmp_path / ".venv" / "ignored.py"

    included.parent.mkdir(parents=True)
    excluded.parent.mkdir(parents=True)

    included.write_text("", encoding="utf-8")
    excluded.write_text("", encoding="utf-8")

    result = find_python_files(tmp_path)

    assert included in result
    assert excluded not in result


def test_write_new_file_creates_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "file.txt"

    write_new_file(path, "content")

    assert path.read_text(encoding="utf-8") == "content"


def test_write_new_file_refuses_to_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        write_new_file(path, "replacement")
