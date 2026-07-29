"""Utilities for desktop notifications."""

import subprocess

from .command_utils import find_command


def notify(title: str, message: str) -> None:
    """Show a desktop notification when notify-send is installed."""

    notify_send = find_command(["notify-send"])

    if not notify_send:
        return

    subprocess.Popen(
        [notify_send, title, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
