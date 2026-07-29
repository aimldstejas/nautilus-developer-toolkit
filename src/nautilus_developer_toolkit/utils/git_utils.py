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


def convert_git_remote_to_web_url(remote_url: str) -> str | None:
    """Convert common Git SSH remotes into browser URLs."""

    remote_url = remote_url.strip()

    if remote_url.startswith("git@"):
        host_and_path = remote_url[4:]

        if ":" not in host_and_path:
            return None

        host, repository_path = host_and_path.split(":", 1)
        remote_url = f"https://{host}/{repository_path}"

    elif remote_url.startswith("ssh://git@"):
        remote_url = "https://" + remote_url[len("ssh://git@") :]

    elif remote_url.startswith("git://"):
        remote_url = "https://" + remote_url[len("git://") :]

    elif not remote_url.startswith(("http://", "https://")):
        return None

    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    return remote_url
