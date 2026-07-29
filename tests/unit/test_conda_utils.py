"""Tests for Conda discovery utilities."""

import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest

from nautilus_developer_toolkit.utils.conda_utils import (
    build_conda_shell_command,
    find_conda_executable,
    get_conda_environments,
    read_conda_environment_name,
)


def test_find_conda_executable_returns_path_discovery_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CONDA_EXE", raising=False)
    monkeypatch.setattr("shutil.which", lambda command: "/usr/bin/conda")
    monkeypatch.setattr(Path, "is_file", lambda path: str(path) == "/usr/bin/conda")

    assert find_conda_executable() == "/usr/bin/conda"


def test_find_conda_executable_falls_back_to_home_directory_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CONDA_EXE", raising=False)
    monkeypatch.setattr(Path, "home", lambda: Path("/home/tester"))
    monkeypatch.setattr("shutil.which", lambda command: None)
    monkeypatch.setattr(
        Path,
        "is_file",
        lambda path: str(path) == "/home/tester/miniconda3/bin/conda",
    )

    assert find_conda_executable() == "/home/tester/miniconda3/bin/conda"


def test_find_conda_executable_returns_none_when_no_candidate_exists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CONDA_EXE", raising=False)
    monkeypatch.setattr("shutil.which", lambda command: None)
    monkeypatch.setattr(Path, "is_file", lambda path: False)

    assert find_conda_executable() is None


def test_find_conda_executable_preserves_search_order(monkeypatch: pytest.MonkeyPatch) -> None:
    checked_paths: list[str] = []

    monkeypatch.setenv("CONDA_EXE", "/env/conda")
    monkeypatch.setattr(Path, "home", lambda: Path("/home/tester"))
    monkeypatch.setattr("shutil.which", lambda command: "/usr/bin/conda")

    def fake_is_file(path: Path) -> bool:
        checked_paths.append(str(path))
        return False

    monkeypatch.setattr(Path, "is_file", fake_is_file)

    assert find_conda_executable() is None
    assert checked_paths == [
        "/env/conda",
        "/home/tester/miniconda3/bin/conda",
        "/home/tester/anaconda3/bin/conda",
        "/home/tester/miniforge3/bin/conda",
        "/home/tester/mambaforge/bin/conda",
        "/opt/conda/bin/conda",
        "/usr/bin/conda",
    ]


def test_build_conda_shell_command_returns_existing_simple_command() -> None:
    command = build_conda_shell_command(
        "/opt/conda/bin/conda",
        "/opt/conda/envs/development",
        "/workspace/project",
    )

    assert command == (
        "source /opt/conda/etc/profile.d/conda.sh; "
        "conda activate /opt/conda/envs/development; "
        "cd /workspace/project; "
        'echo "Active Conda environment: $CONDA_DEFAULT_ENV"; '
        'echo "Working directory: $(pwd)"; '
        "exec bash"
    )


def test_build_conda_shell_command_preserves_application_command() -> None:
    command = build_conda_shell_command(
        "/opt/conda/bin/conda",
        "/opt/conda/envs/development",
        "/workspace/project",
        "streamlit run app.py",
    )

    assert command.endswith(
        "if command -v streamlit run app.py >/dev/null 2>&1; "
        "then streamlit run app.py; "
        "else echo 'streamlit run app.py is not installed in this environment.'; echo; fi; "
        "exec bash"
    )


def test_build_conda_shell_command_quotes_paths_with_spaces() -> None:
    command = build_conda_shell_command(
        "/home/tester/miniconda 3/bin/conda",
        "/home/tester/miniconda 3/envs/my environment",
        "/workspace/project folder",
    )

    assert command.startswith(
        "source '/home/tester/miniconda 3/etc/profile.d/conda.sh'; "
        "conda activate '/home/tester/miniconda 3/envs/my environment'; "
        "cd '/workspace/project folder'; "
    )


def test_get_conda_environments_returns_empty_when_conda_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.conda_utils.find_conda_executable",
        lambda: None,
    )

    assert get_conda_environments() == []


def test_get_conda_environments_uses_existing_conda_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(stdout=json.dumps({"envs": []}))

    monkeypatch.setattr("subprocess.run", fake_run)

    assert get_conda_environments("/opt/conda/bin/conda") == []
    assert captured == {
        "command": ["/opt/conda/bin/conda", "env", "list", "--json"],
        "kwargs": {
            "capture_output": True,
            "text": True,
            "check": True,
            "timeout": 15,
        },
    }


def test_get_conda_environments_parses_names_and_sorts_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(
            stdout=json.dumps(
                {
                    "envs": [
                        "/home/tester/miniconda3/envs/Zulu",
                        "/home/tester/miniconda3",
                        "/home/tester/miniconda3/envs/alpha",
                    ]
                }
            )
        )

    monkeypatch.setattr("subprocess.run", fake_run)

    assert get_conda_environments("/opt/conda/bin/conda") == [
        ("base", "/home/tester/miniconda3"),
        ("alpha", "/home/tester/miniconda3/envs/alpha"),
        ("Zulu", "/home/tester/miniconda3/envs/Zulu"),
    ]


def test_get_conda_environments_returns_empty_and_notifies_on_command_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notifications: list[tuple[str, str]] = []

    def fail_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        raise subprocess.CalledProcessError(1, command)

    monkeypatch.setattr("subprocess.run", fail_run)
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.conda_utils.notify",
        lambda title, message: notifications.append((title, message)),
    )

    assert get_conda_environments("/opt/conda/bin/conda") == []
    assert notifications[0][0] == "Conda environment error"


def test_get_conda_environments_returns_empty_and_notifies_on_invalid_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notifications: list[tuple[str, str]] = []

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(stdout="not valid JSON")

    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.conda_utils.notify",
        lambda title, message: notifications.append((title, message)),
    )

    assert get_conda_environments("/opt/conda/bin/conda") == []
    assert notifications[0][0] == "Conda environment error"


def test_read_conda_environment_name_returns_first_nonempty_name(tmp_path: Path) -> None:
    environment_file = tmp_path / "environment.yml"
    environment_file.write_text(
        "name: first-environment\nname: second-environment\n",
        encoding="utf-8",
    )

    assert read_conda_environment_name(environment_file) == "first-environment"


def test_read_conda_environment_name_strips_surrounding_whitespace(tmp_path: Path) -> None:
    environment_file = tmp_path / "environment.yml"
    environment_file.write_text("  name:  development  \n", encoding="utf-8")

    assert read_conda_environment_name(environment_file) == "development"


@pytest.mark.parametrize(
    "contents",
    [
        "",
        "   \n\t",
        "channels:\n  - conda-forge\n",
        "name:\n",
    ],
)
def test_read_conda_environment_name_returns_none_for_empty_or_malformed_content(
    tmp_path: Path,
    contents: str,
) -> None:
    environment_file = tmp_path / "environment.yml"
    environment_file.write_text(contents, encoding="utf-8")

    assert read_conda_environment_name(environment_file) is None


def test_read_conda_environment_name_returns_none_for_missing_file(tmp_path: Path) -> None:
    assert read_conda_environment_name(tmp_path / "environment.yml") is None


def test_read_conda_environment_name_returns_none_for_directory(tmp_path: Path) -> None:
    environment_file = tmp_path / "environment.yml"
    environment_file.mkdir()

    assert read_conda_environment_name(environment_file) is None


def test_read_conda_environment_name_ignores_invalid_utf8_bytes(tmp_path: Path) -> None:
    environment_file = tmp_path / "environment.yml"
    environment_file.write_bytes(b"\xffname: byte-safe\n")

    assert read_conda_environment_name(environment_file) == "byte-safe"


def test_read_conda_environment_name_returns_none_for_read_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    environment_file = tmp_path / "environment.yml"

    def fail_read_text(path: Path, **kwargs: object) -> str:
        raise PermissionError("permission denied")

    monkeypatch.setattr(Path, "read_text", fail_read_text)

    assert read_conda_environment_name(environment_file) is None


def test_read_conda_environment_name_wrapper_forwards_original_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
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

    received: list[Path] = []

    def fake_read_environment_name(environment_file: Path) -> str:
        received.append(environment_file)
        return "delegated-environment"

    monkeypatch.setattr(
        context_menu_module,
        "read_environment_name_from_file",
        fake_read_environment_name,
    )
    environment_file = tmp_path / "environment.yml"

    assert (
        context_menu_module.DeveloperContextMenu.read_conda_environment_name(environment_file)
        == "delegated-environment"
    )
    assert received == [environment_file]
