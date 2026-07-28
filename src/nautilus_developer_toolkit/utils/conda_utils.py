"""Utilities for discovering Conda installations."""

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path

from .notification_utils import notify


def find_conda_executable() -> str | None:
    """Find Conda without relying only on Nautilus's PATH."""

    candidates = [
        os.environ.get("CONDA_EXE"),
        str(Path.home() / "miniconda3" / "bin" / "conda"),
        str(Path.home() / "anaconda3" / "bin" / "conda"),
        str(Path.home() / "miniforge3" / "bin" / "conda"),
        str(Path.home() / "mambaforge" / "bin" / "conda"),
        "/opt/conda/bin/conda",
        shutil.which("conda"),
    ]

    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate

    return None


def get_conda_environments(conda_executable: str | None = None) -> list[tuple[str, str]]:
    """Return Conda environments as name/path tuples."""

    conda_executable = conda_executable or find_conda_executable()

    if not conda_executable:
        return []

    try:
        result = subprocess.run(
            [conda_executable, "env", "list", "--json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )

        data = json.loads(result.stdout)
        environment_paths = data.get("envs", [])

        environments: list[tuple[str, str]] = []

        for environment_path in environment_paths:
            path = Path(environment_path)
            name = path.name

            if name in {
                "miniconda3",
                "anaconda3",
                "miniforge3",
                "mambaforge",
            }:
                name = "base"

            environments.append((name, str(path)))

        environments.sort(
            key=lambda item: (
                item[0] != "base",
                item[0].lower(),
            )
        )

        return environments

    except Exception as error:
        notify(
            "Conda environment error",
            f"Could not read Conda environments: {error}",
        )
        return []


def build_conda_shell_command(
    conda_executable: str,
    environment_path: str,
    folder_path: str,
    application_command: str | None = None,
) -> str:
    """Build a shell command that activates a Conda environment."""

    conda_root = Path(conda_executable).parent.parent
    conda_script = conda_root / "etc" / "profile.d" / "conda.sh"

    quoted_folder = shlex.quote(folder_path)
    quoted_environment = shlex.quote(environment_path)
    quoted_conda_script = shlex.quote(str(conda_script))

    command_parts = [
        f"source {quoted_conda_script}",
        f"conda activate {quoted_environment}",
        f"cd {quoted_folder}",
        'echo "Active Conda environment: $CONDA_DEFAULT_ENV"',
        'echo "Working directory: $(pwd)"',
    ]

    if application_command:
        quoted_message = shlex.quote(f"{application_command} is not installed in this environment.")

        command_parts.append(
            f"if command -v {application_command} >/dev/null 2>&1; "
            f"then {application_command}; "
            f"else echo {quoted_message}; echo; fi"
        )

    command_parts.append("exec bash")

    return "; ".join(command_parts)
