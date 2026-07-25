"""Filesystem-related utility functions."""

from pathlib import Path


def search_upwards(
    folder_path: str,
    names: list[str],
) -> Path | None:
    """Search the selected folder and its parents for a marker."""

    current = Path(folder_path).expanduser().resolve()

    for directory in [current, *current.parents]:
        for name in names:
            candidate = directory / name

            if candidate.exists():
                return candidate

    return None


def file_contains_any(path: Path, patterns: list[str]) -> bool:
    """Return True when a text file contains any supplied pattern."""

    try:
        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).lower()
    except OSError:
        return False

    return any(pattern.lower() in content for pattern in patterns)


def find_python_files(root: Path) -> list[Path]:
    """Return likely Python entry files while skipping large folders."""

    skipped_parts = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "site-packages",
        "dist",
        "build",
    }

    files: list[Path] = []

    try:
        for path in root.rglob("*.py"):
            if any(part in skipped_parts for part in path.parts):
                continue

            files.append(path)

            if len(files) >= 300:
                break
    except OSError:
        pass

    return files


def write_new_file(path: Path, content: str) -> None:
    """Create a file without overwriting an existing file."""

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")

    path.write_text(content, encoding="utf-8")
