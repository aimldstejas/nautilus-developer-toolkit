"""Path-related utility functions."""

from pathlib import Path
from typing import Any, cast


def module_name_from_file(
    project_root: str,
    entry_file: str,
) -> str:
    """Convert a Python path into an importable module name."""

    relative = Path(entry_file).relative_to(Path(project_root)).with_suffix("")

    return ".".join(relative.parts)


def get_local_path(file_info: Any) -> str | None:
    """Return the local filesystem path for a Nautilus item."""

    location = file_info.get_location()

    if location is None:
        return None

    return cast(str | None, location.get_path())
