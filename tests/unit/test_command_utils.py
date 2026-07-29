"""Tests for command discovery utilities."""

import pytest

from nautilus_developer_toolkit.utils.command_utils import find_command


def test_find_command_returns_first_available(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_which(command: str) -> str | None:
        return "/usr/bin/tool" if command == "tool" else None

    monkeypatch.setattr("shutil.which", fake_which)

    assert find_command(["missing", "tool"]) == "/usr/bin/tool"


def test_find_command_skips_missing_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_which(command: str) -> str | None:
        return "/usr/bin/available" if command == "available" else None

    monkeypatch.setattr("shutil.which", fake_which)

    assert find_command(["missing-one", "missing-two", "available"]) == "/usr/bin/available"


def test_find_command_returns_none_when_no_candidate_is_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("shutil.which", lambda command: None)

    assert find_command(["missing-one", "missing-two"]) is None


def test_find_command_returns_none_for_empty_candidates(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_if_called(command: str) -> None:
        raise AssertionError(f"shutil.which should not be called for an empty list: {command}")

    monkeypatch.setattr("shutil.which", fail_if_called)

    assert find_command([]) is None


def test_find_command_preserves_candidate_order(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_which(command: str) -> str | None:
        calls.append(command)
        return f"/usr/bin/{command}" if command in {"first", "second"} else None

    monkeypatch.setattr("shutil.which", fake_which)

    assert find_command(["missing", "first", "second"]) == "/usr/bin/first"
    assert calls == ["missing", "first"]
