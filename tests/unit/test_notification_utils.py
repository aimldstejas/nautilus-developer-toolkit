"""Tests for desktop notification utilities."""

import subprocess

import pytest

from nautilus_developer_toolkit.utils.notification_utils import notify


def test_notify_returns_when_notify_send_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_if_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("subprocess.Popen should not be called when notify-send is missing")

    monkeypatch.setattr("shutil.which", lambda command: None)
    monkeypatch.setattr("subprocess.Popen", fail_if_called)

    notify("Title", "Message")


def test_notify_launches_notify_send_with_expected_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_popen(command: list[str], **kwargs: object) -> None:
        calls.append((command, kwargs))

    monkeypatch.setattr(
        "shutil.which",
        lambda command: "/usr/bin/notify-send" if command == "notify-send" else None,
    )
    monkeypatch.setattr("subprocess.Popen", fake_popen)

    notify("Title", "Message")

    assert calls == [
        (
            ["/usr/bin/notify-send", "Title", "Message"],
            {
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
                "start_new_session": True,
            },
        )
    ]
