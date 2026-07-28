"""Tests for detached process-launch utilities."""

import subprocess

import pytest

from nautilus_developer_toolkit.utils.process_utils import launch_process


def test_launch_process_uses_existing_popen_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    command = ["example", "--flag"]

    def fake_popen(process_command: list[str], **kwargs: object) -> None:
        captured["command"] = process_command
        captured["kwargs"] = kwargs

    monkeypatch.setattr("subprocess.Popen", fake_popen)

    launch_process(command, "/workspace/project", "Example")

    assert captured == {
        "command": command,
        "kwargs": {
            "cwd": "/workspace/project",
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "start_new_session": True,
        },
    }


def test_launch_process_notifies_when_popen_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notifications: list[tuple[str, str]] = []

    def fail_popen(process_command: list[str], **kwargs: object) -> None:
        raise OSError("permission denied")

    monkeypatch.setattr("subprocess.Popen", fail_popen)

    launch_process(
        ["example"],
        "/workspace/project",
        "Example",
        notify_callback=lambda title, message: notifications.append((title, message)),
    )

    assert notifications == [
        (
            "Developer Context Menu",
            "Could not launch Example: permission denied",
        )
    ]


def test_launch_process_ignores_popen_errors_without_callback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_popen(process_command: list[str], **kwargs: object) -> None:
        raise OSError("permission denied")

    monkeypatch.setattr("subprocess.Popen", fail_popen)

    launch_process(["example"], "/workspace/project", "Example")
