"""Utilities for checking Docker Compose availability."""

import subprocess

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
