"""Tests for Git repository-root utilities."""

from types import SimpleNamespace

import pytest

from nautilus_developer_toolkit.utils.git_utils import get_git_root


def test_get_git_root_returns_none_when_git_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.git_utils.find_command",
        lambda candidates: None,
    )

    assert get_git_root("/workspace/project") is None


def test_get_git_root_uses_existing_git_command_and_strips_root(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="/workspace/project\n")

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.git_utils.find_command",
        lambda candidates: "/usr/bin/git",
    )
    monkeypatch.setattr("subprocess.run", fake_run)

    assert get_git_root("/workspace/project/src") == "/workspace/project"
    assert captured == {
        "command": [
            "/usr/bin/git",
            "-C",
            "/workspace/project/src",
            "rev-parse",
            "--show-toplevel",
        ],
        "kwargs": {
            "capture_output": True,
            "text": True,
            "check": False,
            "timeout": 10,
        },
    }


def test_get_git_root_returns_none_for_non_repository_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.git_utils.find_command",
        lambda candidates: "/usr/bin/git",
    )
    monkeypatch.setattr(
        "subprocess.run",
        lambda command, **kwargs: SimpleNamespace(returncode=128, stdout=""),
    )

    assert get_git_root("/workspace/not-a-repository") is None


def test_get_git_root_returns_none_for_empty_output_or_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.git_utils.find_command",
        lambda candidates: "/usr/bin/git",
    )
    monkeypatch.setattr(
        "subprocess.run",
        lambda command, **kwargs: SimpleNamespace(returncode=0, stdout="  \n"),
    )

    assert get_git_root("/workspace/project") is None

    def fail_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        raise OSError("Git unavailable")

    monkeypatch.setattr("subprocess.run", fail_run)

    assert get_git_root("/workspace/project") is None
