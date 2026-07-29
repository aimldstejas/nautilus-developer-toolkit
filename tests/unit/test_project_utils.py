"""Tests for project-detection utility functions."""

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from nautilus_developer_toolkit.utils.project_utils import (
    detect_project,
    detect_project_root,
    project_report,
)


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


def test_detect_project_forwards_root_and_preserves_default_contract(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    received: list[str] = []

    def fake_detect_project_root(folder_path: str) -> str:
        received.append(folder_path)
        return str(tmp_path)

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        fake_detect_project_root,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_compose_file",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_python_files",
        lambda root: [],
    )

    assert detect_project("relative/project") == {
        "root": str(tmp_path.resolve()),
        "git": False,
        "python": False,
        "environment_file": None,
        "local_environment": None,
        "requirements": None,
        "pyproject": None,
        "jupyter": False,
        "streamlit": False,
        "streamlit_entry": None,
        "fastapi": False,
        "fastapi_entry": None,
        "docker": False,
        "compose_file": None,
        "dockerfile": None,
        "modelfile": None,
    }
    assert received == ["relative/project"]


def test_detect_project_propagates_project_root_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_detect_project_root(folder_path: str) -> str:
        raise OSError("root failed")

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        fail_detect_project_root,
    )

    with pytest.raises(OSError, match="root failed"):
        detect_project("project")


def test_detect_project_preserves_environment_and_local_environment_order(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "environment.yml").touch()
    (tmp_path / "environment.yaml").touch()
    for name in [".venv", "venv"]:
        python_path = tmp_path / name / "bin" / "python"
        python_path.parent.mkdir(parents=True)
        python_path.touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        lambda folder_path: str(tmp_path),
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: "/git/root",
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_compose_file",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_python_files",
        lambda root: [],
    )

    project = detect_project("project")

    assert project["git"] is True
    assert project["environment_file"] == str(tmp_path / "environment.yml")
    assert project["local_environment"] == str(tmp_path / ".venv")
    assert project["python"] is True


def test_detect_project_preserves_project_file_and_docker_flags(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    for name in ["requirements.txt", "pyproject.toml", "Dockerfile", "Modelfile"]:
        (tmp_path / name).touch()
    compose_file = tmp_path / "compose.yml"
    compose_file.touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        lambda folder_path: str(tmp_path),
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_compose_file",
        lambda folder_path: str(compose_file),
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_python_files",
        lambda root: [],
    )

    project = detect_project("project")

    assert project["requirements"] == str(tmp_path / "requirements.txt")
    assert project["pyproject"] == str(tmp_path / "pyproject.toml")
    assert project["compose_file"] == str(compose_file)
    assert project["dockerfile"] == str(tmp_path / "Dockerfile")
    assert project["modelfile"] == str(tmp_path / "Modelfile")
    assert project["python"] is True
    assert project["docker"] is True


def test_detect_project_preserves_notebook_detection_and_rglob_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "analysis.ipynb"
    notebook.touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        lambda folder_path: str(tmp_path),
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_compose_file",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_python_files",
        lambda root: [],
    )

    assert detect_project("project")["jupyter"] is True

    def fail_rglob(path: Path, pattern: str) -> list[Path]:
        raise OSError("rglob failed")

    monkeypatch.setattr(Path, "rglob", fail_rglob)

    assert detect_project("project")["jupyter"] is False


def test_detect_project_preserves_streamlit_and_fastapi_preferred_order(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    streamlit_app = tmp_path / "streamlit_app.py"
    other_streamlit = tmp_path / "nested" / "other.py"
    fastapi_main = tmp_path / "api" / "main.py"
    for path in [streamlit_app, other_streamlit, fastapi_main]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.detect_project_root",
        lambda folder_path: str(tmp_path),
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.get_git_root",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_compose_file",
        lambda folder_path: None,
    )
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.find_python_files",
        lambda root: [other_streamlit, streamlit_app, fastapi_main],
    )

    def fake_file_contains_any(path: Path, patterns: list[str]) -> bool:
        if "import streamlit" in patterns:
            return path in {streamlit_app, other_streamlit}
        return path == fastapi_main

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.project_utils.file_contains_any",
        fake_file_contains_any,
    )

    project = detect_project("project")

    assert project["streamlit_entry"] == str(streamlit_app)
    assert project["fastapi_entry"] == str(fastapi_main)
    assert project["streamlit"] is True
    assert project["fastapi"] is True
    assert project["python"] is True


def test_detect_project_wrapper_forwards_original_argument(monkeypatch: pytest.MonkeyPatch) -> None:
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

    expected_project = {"root": "/delegated/root"}
    received: list[str] = []

    def fake_detect_project(folder_path: str) -> dict[str, str]:
        received.append(folder_path)
        return expected_project

    monkeypatch.setattr(context_menu_module, "identify_project", fake_detect_project)

    assert (
        context_menu_module.DeveloperContextMenu().detect_project("relative/project")
        is expected_project
    )
    assert received == ["relative/project"]


def test_project_report_preserves_complete_exact_output() -> None:
    project = {
        "root": "/projects/example",
        "git": True,
        "python": True,
        "jupyter": True,
        "streamlit": True,
        "fastapi": True,
        "docker": True,
        "modelfile": "/projects/example/Modelfile",
        "environment_file": "/projects/example/environment.yml",
        "local_environment": "/projects/example/.venv",
        "requirements": "/projects/example/requirements.txt",
        "pyproject": "/projects/example/pyproject.toml",
        "streamlit_entry": "/projects/example/app.py",
        "fastapi_entry": "/projects/example/api/main.py",
        "compose_file": "/projects/example/compose.yml",
        "dockerfile": "/projects/example/Dockerfile",
    }

    assert project_report(project) == (
        "Project root: /projects/example\n"
        "\n"
        "Detected capabilities\n"
        "Git repository: Yes\n"
        "Python project: Yes\n"
        "Jupyter notebooks: Yes\n"
        "Streamlit application: Yes\n"
        "FastAPI application: Yes\n"
        "Docker project: Yes\n"
        "Ollama Modelfile: Yes\n"
        "\n"
        "Detected details\n"
        "Environment file: /projects/example/environment.yml\n"
        "Local environment: /projects/example/.venv\n"
        "Requirements: /projects/example/requirements.txt\n"
        "pyproject.toml: /projects/example/pyproject.toml\n"
        "Streamlit entry: /projects/example/app.py\n"
        "FastAPI entry: /projects/example/api/main.py\n"
        "Compose file: /projects/example/compose.yml\n"
        "Dockerfile: /projects/example/Dockerfile\n"
        "Modelfile: /projects/example/Modelfile"
    )


def test_project_report_omits_falsey_details_and_preserves_default_output() -> None:
    project = {
        "root": "/projects/example",
        "git": False,
        "python": False,
        "jupyter": False,
        "streamlit": False,
        "fastapi": False,
        "docker": False,
        "modelfile": None,
        "environment_file": "",
        "local_environment": None,
        "requirements": False,
        "pyproject": 0,
        "streamlit_entry": [],
        "fastapi_entry": {},
        "compose_file": (),
        "dockerfile": None,
    }

    report = project_report(project)

    assert report == (
        "Project root: /projects/example\n"
        "\n"
        "Detected capabilities\n"
        "Git repository: No\n"
        "Python project: No\n"
        "Jupyter notebooks: No\n"
        "Streamlit application: No\n"
        "FastAPI application: No\n"
        "Docker project: No\n"
        "Ollama Modelfile: No\n"
        "\n"
        "Detected details\n"
        "No recognized project files were found."
    )
    assert not report.endswith("\n")


def test_project_report_wrapper_forwards_original_argument(monkeypatch: pytest.MonkeyPatch) -> None:
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

    expected_project = {"root": "/delegated/root"}
    received: list[dict[str, object]] = []

    def fake_project_report(project: dict[str, object]) -> str:
        received.append(project)
        return "delegated report"

    monkeypatch.setattr(context_menu_module, "build_project_report", fake_project_report)

    assert (
        context_menu_module.DeveloperContextMenu().project_report(expected_project)
        == "delegated report"
    )
    assert received == [expected_project]
