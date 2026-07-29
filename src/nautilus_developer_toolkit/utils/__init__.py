"""Shared utility functions for Nautilus Developer Toolkit."""

from .command_utils import find_command
from .conda_utils import (
    build_conda_shell_command,
    find_conda_executable,
    get_conda_environments,
    read_conda_environment_name,
)
from .docker_utils import docker_compose_available, find_compose_file
from .filesystem import (
    file_contains_any,
    find_python_files,
    search_upwards,
    write_new_file,
)
from .git_utils import convert_git_remote_to_web_url, get_git_remote_url, get_git_root
from .menu_utils import create_menu_item
from .notification_utils import notify
from .paths import get_local_path, module_name_from_file
from .process_utils import launch_process
from .project_utils import detect_project, detect_project_root, project_report

__all__ = [
    "build_conda_shell_command",
    "docker_compose_available",
    "find_compose_file",
    "file_contains_any",
    "find_command",
    "find_conda_executable",
    "get_conda_environments",
    "read_conda_environment_name",
    "get_git_root",
    "convert_git_remote_to_web_url",
    "create_menu_item",
    "get_git_remote_url",
    "get_local_path",
    "find_python_files",
    "module_name_from_file",
    "launch_process",
    "notify",
    "detect_project",
    "detect_project_root",
    "project_report",
    "search_upwards",
    "write_new_file",
]
