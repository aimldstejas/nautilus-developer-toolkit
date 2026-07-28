"""Shared utility functions for Nautilus Developer Toolkit."""

from .command_utils import find_command
from .conda_utils import (
    build_conda_shell_command,
    find_conda_executable,
    get_conda_environments,
)
from .docker_utils import docker_compose_available, find_compose_file
from .filesystem import (
    file_contains_any,
    find_python_files,
    search_upwards,
    write_new_file,
)
from .git_utils import convert_git_remote_to_web_url, get_git_remote_url, get_git_root
from .notification_utils import notify
from .paths import get_local_path, module_name_from_file
from .process_utils import launch_process

__all__ = [
    "build_conda_shell_command",
    "docker_compose_available",
    "find_compose_file",
    "file_contains_any",
    "find_command",
    "find_conda_executable",
    "get_conda_environments",
    "get_git_root",
    "convert_git_remote_to_web_url",
    "get_git_remote_url",
    "get_local_path",
    "find_python_files",
    "module_name_from_file",
    "launch_process",
    "notify",
    "search_upwards",
    "write_new_file",
]
