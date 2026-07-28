"""Utilities for discovering Git repository roots."""

import subprocess

from .command_utils import find_command


def get_git_root(folder_path: str) -> str | None:
    """Return the repository root containing the selected folder."""

    git = find_command(["git"])

    if not git:
        return None

    try:
        result = subprocess.run(
            [
                git,
                "-C",
                folder_path,
                "rev-parse",
                "--show-toplevel",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

        if result.returncode != 0:
            return None

        git_root = result.stdout.strip()

        if not git_root:
            return None

        return git_root

    except Exception:
        return None


def get_git_remote_url(repository_path: str) -> str | None:
    """Return the origin remote URL for a Git repository."""

    git = find_command(["git"])

    if not git:
        return None

    try:
        result = subprocess.run(
            [
                git,
                "-C",
                repository_path,
                "remote",
                "get-url",
                "origin",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

        if result.returncode != 0:
            return None

        remote_url = result.stdout.strip()

        if not remote_url:
            return None

        return remote_url

    except Exception:
        return None
