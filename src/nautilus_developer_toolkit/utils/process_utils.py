"""Utilities for launching detached processes."""

import subprocess
from collections.abc import Callable


def launch_process(
    command: list[str],
    working_directory: str,
    application_name: str,
    notify_callback: Callable[[str, str], None] | None = None,
) -> None:
    """Launch an application safely."""

    try:
        subprocess.Popen(
            command,
            cwd=working_directory,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as error:
        if notify_callback:
            notify_callback(
                "Developer Context Menu",
                f"Could not launch {application_name}: {error}",
            )
