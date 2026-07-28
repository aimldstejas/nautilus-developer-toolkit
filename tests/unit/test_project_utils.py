"""Tests for project-detection utility functions."""

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from nautilus_developer_toolkit.utils.project_utils import detect_project_root


def test_detect_project_root_returns_git_root_before_marker_search(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    project_path = tmp_path / "project"
    project_path.mkdir()
    (project_path / "pyproject.toml").touch()
    searched = False

    def fail_search(folder_path: str, names: list[str]) -> Path | None:
        nonlocal searched
        searched = True
        return None

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: "/git/root",
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.search_upwards",
        fail_search,
    )

    assert detect_project_root(str(project_path)) == "/git/root"
    assert not searched


def test_detect_project_root_returns_current_directory_marker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    project_path = tmp_path / "project"
    project_path.mkdir()
    (project_path / "pyproject.toml").touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root(str(project_path)) == str(project_path)


def test_detect_project_root_returns_nearest_parent_marker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    outer_project = tmp_path / "outer"
    inner_project = outer_project / "inner"
    nested_path = inner_project / "src" / "package"
    nested_path.mkdir(parents=True)
    (outer_project / "pyproject.toml").touch()
    (inner_project / "requirements.txt").touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root(str(nested_path)) == str(inner_project)


def test_detect_project_root_preserves_marker_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received_names: list[str] = []

    def fake_search(folder_path: str, names: list[str]) -> Path | None:
        received_names.extend(names)
        return None

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.search_upwards",
        fake_search,
    )

    detect_project_root("project")

    assert received_names == [
        "pyproject.toml",
        "requirements.txt",
        "environment.yml",
        "environment.yaml",
        "Pipfile",
        "poetry.lock",
        "uv.lock",
        "compose.yml",
        "compose.yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
        "Modelfile",
        ".venv",
        "venv",
    ]


def test_detect_project_root_recognizes_directory_markers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    project_path = tmp_path / "project"
    nested_path = project_path / "src"
    nested_path.mkdir(parents=True)
    (project_path / ".venv").mkdir()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root(str(nested_path)) == str(project_path)


def test_detect_project_root_preserves_file_path_behavior(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    project_path = tmp_path / "project"
    project_path.mkdir()
    file_path = project_path / "entry.py"
    file_path.touch()
    (project_path / "pyproject.toml").touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root(str(file_path)) == str(project_path)


def test_detect_project_root_returns_resolved_input_without_marker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "standalone.py"
    file_path.touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root(str(file_path)) == str(file_path.resolve())


def test_detect_project_root_resolves_relative_and_nonexistent_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )

    assert detect_project_root("missing/project") == str((tmp_path / "missing/project").resolve())


def test_detect_project_root_preserves_filesystem_root_behavior(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.search_upwards",
        lambda folder_path, names: None,
    )

    assert detect_project_root("/") == "/"


def test_detect_project_root_propagates_search_upwards_exceptions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_search(folder_path: str, names: list[str]) -> Path | None:
        raise OSError("search failed")

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.search_upwards",
        fail_search,
    )

    with pytest.raises(OSError, match="search failed"):
        detect_project_root("project")


def test_detect_project_root_wrapper_forwards_original_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gi_module: Any = ModuleType("gi")

    def require_version(namespace: str, version: str) -> None:
        return None

    gi_module.require_version = require_version
    repository_module: Any = ModuleType("gi.repository")

    class FakeGObject:
        class GObject:
            pass

    class FakeNautilus:
        class FileInfo:
            pass

        class Menu:
            pass

        class MenuProvider:
            pass

        class MenuItem:
            pass

    repository_module.GObject = FakeGObject
    repository_module.Nautilus = FakeNautilus
    monkeypatch.setitem(sys.modules, "gi", gi_module)
    monkeypatch.setitem(sys.modules, "gi.repository", repository_module)
    monkeypatch.delitem(sys.modules, "developer_context_menu", raising=False)
    context_menu_module = importlib.import_module("developer_context_menu")

    received: list[str] = []

    def fake_detect_project_root(folder_path: str) -> str:
        received.append(folder_path)
        return "/delegated/root"

    monkeypatch.setattr(context_menu_module, "find_project_root", fake_detect_project_root)

    assert context_menu_module.DeveloperContextMenu().detect_project_root("relative/project") == (
        "/delegated/root"
    )
    assert received == ["relative/project"]
