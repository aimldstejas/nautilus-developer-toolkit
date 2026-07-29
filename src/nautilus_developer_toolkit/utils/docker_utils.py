"""Utilities for checking Docker Compose availability."""

import subprocess
from pathlib import Path

from .command_utils import find_command


def docker_compose_available() -> bool:
    """Check whether the Docker Compose command is available."""

    docker = find_command(["docker"])

    if not docker:
        return False

    try:
        result = subprocess.run(
            [docker, "compose", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=10,
        )

        return result.returncode == 0

    except Exception:
        return False


def find_compose_file(folder_path: str) -> str | None:
    """Find a Docker Compose file in the selected folder."""

    candidates = [
        "compose.yml",
        "compose.yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
    ]

    for candidate in candidates:
        compose_path = Path(folder_path) / candidate

        if compose_path.is_file():
            return str(compose_path)

    return None
