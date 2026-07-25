"""Path-related utility functions."""

from pathlib import Path


def module_name_from_file(
    project_root: str,
    entry_file: str,
) -> str:
    """Convert a Python path into an importable module name."""

    relative = Path(entry_file).relative_to(Path(project_root)).with_suffix("")

    return ".".join(relative.parts)
