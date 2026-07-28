"""Utilities for discovering installed system commands."""

import shutil
from collections.abc import Iterable


def find_command(candidates: Iterable[str]) -> str | None:
    """Return the first installed executable from a list of candidate names."""

    for candidate in candidates:
        command = shutil.which(candidate)

        if command:
            return command

    return None
