"""Tests for Conda discovery utilities."""

from pathlib import Path

import pytest

from nautilus_developer_toolkit.utils.conda_utils import (
    build_conda_shell_command,
    find_conda_executable,
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
