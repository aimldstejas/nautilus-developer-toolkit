"""Project-detection utility functions."""

from pathlib import Path

from .filesystem import search_upwards
from .git_utils import get_git_root


def detect_project_root(folder_path: str) -> str:
    """Return the most likely project root."""

    git_root = get_git_root(folder_path)

    if git_root:
        return git_root

    markers = [
        "pyproject.toml",
        "requirements.txt",
        "environment.yml",
        "environment.yaml",
        "Pipfile",
        "poetry.lock",
        "uv.lock",
        "compose.yml",
        "compose.yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
        "Modelfile",
        ".venv",
        "venv",
    ]

    marker = search_upwards(folder_path, markers)

    if marker:
        return str(marker.parent)

    return str(Path(folder_path).expanduser().resolve())
