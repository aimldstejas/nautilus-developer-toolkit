"""Tests for Docker Compose utilities."""

import subprocess
from types import SimpleNamespace

import pytest

from nautilus_developer_toolkit.utils.docker_utils import docker_compose_available


def test_missing_docker_returns_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.docker_utils.find_command", lambda candidates: None
    )
    assert docker_compose_available() is False


def test_docker_compose_command_and_success(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.docker_utils.find_command",
        lambda candidates: "/usr/bin/docker",
    )
    monkeypatch.setattr("subprocess.run", fake_run)
    assert docker_compose_available() is True
    assert captured == {
        "command": ["/usr/bin/docker", "compose", "version"],
        "kwargs": {
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "check": False,
            "timeout": 10,
        },
    }


def test_docker_compose_nonzero_or_exception_returns_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "nautilus_developer_toolkit.utils.docker_utils.find_command",
        lambda candidates: "/usr/bin/docker",
    )
    monkeypatch.setattr("subprocess.run", lambda command, **kwargs: SimpleNamespace(returncode=1))
    assert docker_compose_available() is False

    def fail_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        raise OSError("missing")

    monkeypatch.setattr("subprocess.run", fail_run)
    assert docker_compose_available() is False
