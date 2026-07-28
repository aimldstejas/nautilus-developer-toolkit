"""Utilities for discovering Conda installations."""

import os
import shutil
from pathlib import Path


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
