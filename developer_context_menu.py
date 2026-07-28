#!/usr/bin/env python3

import json
import shlex
import shutil
import subprocess
from pathlib import Path

import gi

gi.require_version("Nautilus", "4.0")

from gi.repository import GObject, Nautilus  # noqa: E402

from nautilus_developer_toolkit.utils import (  # noqa: E402
    file_contains_any,
    find_python_files,
    module_name_from_file,
    search_upwards,
    write_new_file,
)
from nautilus_developer_toolkit.utils import find_command as find_system_command  # noqa: E402
from nautilus_developer_toolkit.utils import find_conda_executable as find_conda_path  # noqa: E402
from nautilus_developer_toolkit.utils import notify as send_desktop_notification  # noqa: E402


class DeveloperContextMenu(GObject.GObject, Nautilus.MenuProvider):
    """Structured Developer context menu for GNOME Files."""

    # ================================================================
    # General helpers
    # ================================================================

    @staticmethod
    def get_local_path(file_info: Nautilus.FileInfo) -> str | None:
        """Return the local filesystem path for a Nautilus item."""

        location = file_info.get_location()

        if location is None:
            return None

        return location.get_path()

    @staticmethod
    def find_command(candidates: list[str]) -> str | None:
        """Return the first installed executable from a list."""

        return find_system_command(candidates)

    @staticmethod
    def notify(title: str, message: str) -> None:
        """Show a desktop notification when notify-send is installed."""

        send_desktop_notification(title, message)

    def launch_process(
        self,
        command: list[str],
        working_directory: str,
        application_name: str,
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
            self.notify(
                "Developer Context Menu",
                f"Could not launch {application_name}: {error}",
            )

    @staticmethod
    def create_menu_item(
        name: str,
        label: str,
        tip: str,
        icon: str,
    ) -> Nautilus.MenuItem:
        """Create one Nautilus menu item."""

        return Nautilus.MenuItem(
            name=name,
            label=label,
            tip=tip,
            icon=icon,
        )

    def run_terminal_command(
        self,
        folder_path: str,
        command: str,
        title: str,
        keep_open: bool = True,
    ) -> None:
        """Run a shell command in GNOME Terminal."""

        terminal = self.find_command(["gnome-terminal"])

        if not terminal:
            self.notify(
                "Terminal not found",
                "The gnome-terminal executable could not be found.",
            )
            return

        quoted_folder = shlex.quote(folder_path)

        shell_parts = [
            f"cd {quoted_folder}",
            f"printf '\\033]0;{title}\\007'",
            command,
        ]

        if keep_open:
            shell_parts.extend(
                [
                    "echo",
                    'echo "Press Enter to close this terminal."',
                    "read -r",
                ]
            )

        shell_command = "; ".join(shell_parts)

        self.launch_process(
            [
                terminal,
                "--working-directory",
                folder_path,
                "--",
                "bash",
                "-lc",
                shell_command,
            ],
            folder_path,
            title,
        )

    def open_interactive_terminal_command(
        self,
        folder_path: str,
        setup_command: str,
        title: str,
    ) -> None:
        """Open an interactive terminal after running setup commands."""

        terminal = self.find_command(["gnome-terminal"])

        if not terminal:
            self.notify(
                "Terminal not found",
                "The gnome-terminal executable could not be found.",
            )
            return

        quoted_folder = shlex.quote(folder_path)

        shell_command = "; ".join(
            [
                f"cd {quoted_folder}",
                f"printf '\\033]0;{title}\\007'",
                setup_command,
                "exec bash",
            ]
        )

        self.launch_process(
            [
                terminal,
                "--working-directory",
                folder_path,
                "--",
                "bash",
                "-lc",
                shell_command,
            ],
            folder_path,
            title,
        )

    # ================================================================
    # Conda helpers
    # ================================================================

    @staticmethod
    def find_conda_executable() -> str | None:
        """Find Conda without relying only on Nautilus's PATH."""

        return find_conda_path()

    def get_conda_environments(self) -> list[tuple[str, str]]:
        """Return Conda environments as name/path tuples."""

        conda_executable = self.find_conda_executable()

        if not conda_executable:
            return []

        try:
            result = subprocess.run(
                [conda_executable, "env", "list", "--json"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15,
            )

            data = json.loads(result.stdout)
            environment_paths = data.get("envs", [])

            environments: list[tuple[str, str]] = []

            for environment_path in environment_paths:
                path = Path(environment_path)
                name = path.name

                if name in {
                    "miniconda3",
                    "anaconda3",
                    "miniforge3",
                    "mambaforge",
                }:
                    name = "base"

                environments.append((name, str(path)))

            environments.sort(
                key=lambda item: (
                    item[0] != "base",
                    item[0].lower(),
                )
            )

            return environments

        except Exception as error:
            self.notify(
                "Conda environment error",
                f"Could not read Conda environments: {error}",
            )
            return []

    def choose_conda_environment(self) -> str | None:
        """Display a graphical Conda environment selector."""

        environments = self.get_conda_environments()

        if not environments:
            self.notify(
                "No Conda environments found",
                "Conda is unavailable or no environments were detected.",
            )
            return None

        zenity = shutil.which("zenity")

        if not zenity:
            self.notify(
                "Zenity not installed",
                "Install Zenity to use the environment selector.",
            )
            return None

        command = [
            zenity,
            "--list",
            "--title=Select Conda Environment",
            "--text=Choose the Conda environment to use:",
            "--width=700",
            "--height=550",
            "--column=Environment",
            "--column=Path",
            "--print-column=2",
        ]

        for environment_name, environment_path in environments:
            command.extend(
                [
                    environment_name,
                    environment_path,
                ]
            )

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return None

            selected_path = result.stdout.strip()

            if not selected_path:
                return None

            return selected_path

        except Exception as error:
            self.notify(
                "Environment selector error",
                f"Could not display the selector: {error}",
            )
            return None

    def build_conda_shell_command(
        self,
        environment_path: str,
        folder_path: str,
        application_command: str | None = None,
    ) -> str:
        """Build a shell command that activates a Conda environment."""

        conda_executable = self.find_conda_executable()

        if not conda_executable:
            raise RuntimeError("Conda executable was not found.")

        conda_root = Path(conda_executable).parent.parent
        conda_script = conda_root / "etc" / "profile.d" / "conda.sh"

        quoted_folder = shlex.quote(folder_path)
        quoted_environment = shlex.quote(environment_path)
        quoted_conda_script = shlex.quote(str(conda_script))

        command_parts = [
            f"source {quoted_conda_script}",
            f"conda activate {quoted_environment}",
            f"cd {quoted_folder}",
            'echo "Active Conda environment: $CONDA_DEFAULT_ENV"',
            'echo "Working directory: $(pwd)"',
        ]

        if application_command:
            quoted_message = shlex.quote(
                f"{application_command} is not installed in this environment."
            )

            command_parts.append(
                f"if command -v {application_command} >/dev/null 2>&1; "
                f"then {application_command}; "
                f"else echo {quoted_message}; echo; fi"
            )

        command_parts.append("exec bash")

        return "; ".join(command_parts)

    def open_conda_terminal(
        self,
        environment_path: str,
        folder_path: str,
        application_command: str | None = None,
    ) -> None:
        """Open GNOME Terminal with a selected Conda environment."""

        terminal = self.find_command(["gnome-terminal"])

        if not terminal:
            self.notify(
                "Terminal not found",
                "The gnome-terminal executable could not be found.",
            )
            return

        try:
            shell_command = self.build_conda_shell_command(
                environment_path=environment_path,
                folder_path=folder_path,
                application_command=application_command,
            )

            self.launch_process(
                [
                    terminal,
                    "--working-directory",
                    folder_path,
                    "--",
                    "bash",
                    "-lc",
                    shell_command,
                ],
                folder_path,
                "Conda Terminal",
            )

        except Exception as error:
            self.notify(
                "Conda launch error",
                str(error),
            )

    def select_and_launch_conda_tool(
        self,
        folder_path: str,
        application_command: str | None = None,
    ) -> None:
        """Choose an environment and launch a Conda-aware command."""

        environment_path = self.choose_conda_environment()

        if not environment_path:
            return

        self.open_conda_terminal(
            environment_path=environment_path,
            folder_path=folder_path,
            application_command=application_command,
        )

    # ================================================================
    # Git helpers
    # ================================================================

    def get_git_root(self, folder_path: str) -> str | None:
        """Return the repository root containing the selected folder."""

        git = self.find_command(["git"])

        if not git:
            return None

        try:
            result = subprocess.run(
                [
                    git,
                    "-C",
                    folder_path,
                    "rev-parse",
                    "--show-toplevel",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )

            if result.returncode != 0:
                return None

            git_root = result.stdout.strip()

            if not git_root:
                return None

            return git_root

        except Exception:
            return None

    def get_git_remote_url(self, repository_path: str) -> str | None:
        """Return the origin remote URL for a Git repository."""

        git = self.find_command(["git"])

        if not git:
            return None

        try:
            result = subprocess.run(
                [
                    git,
                    "-C",
                    repository_path,
                    "remote",
                    "get-url",
                    "origin",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )

            if result.returncode != 0:
                return None

            remote_url = result.stdout.strip()

            if not remote_url:
                return None

            return remote_url

        except Exception:
            return None

    @staticmethod
    def convert_git_remote_to_web_url(remote_url: str) -> str | None:
        """Convert common Git SSH remotes into browser URLs."""

        remote_url = remote_url.strip()

        if remote_url.startswith("git@"):
            host_and_path = remote_url[4:]

            if ":" not in host_and_path:
                return None

            host, repository_path = host_and_path.split(":", 1)
            remote_url = f"https://{host}/{repository_path}"

        elif remote_url.startswith("ssh://git@"):
            remote_url = "https://" + remote_url[len("ssh://git@") :]

        elif remote_url.startswith("git://"):
            remote_url = "https://" + remote_url[len("git://") :]

        elif not remote_url.startswith(("http://", "https://")):
            return None

        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]

        return remote_url

    # ================================================================
    # Docker helpers
    # ================================================================

    @staticmethod
    def find_compose_file(folder_path: str) -> str | None:
        """Find a Docker Compose file in the selected folder."""

        candidates = [
            "compose.yml",
            "compose.yaml",
            "docker-compose.yml",
            "docker-compose.yaml",
        ]

        for candidate in candidates:
            compose_path = Path(folder_path) / candidate

            if compose_path.is_file():
                return str(compose_path)

        return None

    def docker_compose_available(self) -> bool:
        """Check whether the Docker Compose command is available."""

        docker = self.find_command(["docker"])

        if not docker:
            return False

        try:
            result = subprocess.run(
                [docker, "compose", "version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=10,
            )

            return result.returncode == 0

        except Exception:
            return False

    # ================================================================
    # Editor actions
    # ================================================================

    def open_gedit(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Launch gedit."""

        command = self.find_command(["gedit"])

        if not command:
            self.notify("gedit not found", "gedit could not be found.")
            return

        self.launch_process(
            [command],
            folder_path,
            "gedit",
        )

    def open_vscodium(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the selected folder in VSCodium."""

        command = self.find_command(
            [
                "codium",
                "codium-insiders",
                "vscodium",
            ]
        )

        if not command:
            self.notify(
                "VSCodium not found",
                "The VSCodium executable could not be found.",
            )
            return

        self.launch_process(
            [command, folder_path],
            folder_path,
            "VSCodium",
        )

    def open_vscode(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the selected folder in Visual Studio Code."""

        command = self.find_command(
            [
                "code",
                "code-insiders",
            ]
        )

        if not command:
            self.notify(
                "Visual Studio Code not found",
                "The code executable could not be found.",
            )
            return

        self.launch_process(
            [command, folder_path],
            folder_path,
            "Visual Studio Code",
        )

    def open_cursor(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the selected folder in Cursor."""

        command = self.find_command(["cursor"])

        if not command:
            self.notify(
                "Cursor not found",
                "The Cursor executable could not be found.",
            )
            return

        self.launch_process(
            [command, folder_path],
            folder_path,
            "Cursor",
        )

    def open_pycharm(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the selected folder in PyCharm."""

        command = self.find_command(
            [
                "pycharm",
                "pycharm-professional",
                "pycharm-community",
                "pycharm.sh",
            ]
        )

        if not command:
            self.notify(
                "PyCharm not found",
                "No PyCharm executable could be found.",
            )
            return

        self.launch_process(
            [command, folder_path],
            folder_path,
            "PyCharm",
        )

    # ================================================================
    # Python and Conda actions
    # ================================================================

    def open_conda_shell(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open a shell after choosing a Conda environment."""

        self.select_and_launch_conda_tool(folder_path=folder_path)

    def start_python_repl(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start Python in a selected Conda environment."""

        self.select_and_launch_conda_tool(
            folder_path=folder_path,
            application_command="python",
        )

    def start_ipython(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start IPython in a selected Conda environment."""

        self.select_and_launch_conda_tool(
            folder_path=folder_path,
            application_command="ipython",
        )

    def start_jupyterlab(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start JupyterLab in a selected Conda environment."""

        self.select_and_launch_conda_tool(
            folder_path=folder_path,
            application_command="jupyter-lab",
        )

    def start_jupyter_notebook(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start Jupyter Notebook in a selected Conda environment."""

        self.select_and_launch_conda_tool(
            folder_path=folder_path,
            application_command="jupyter-notebook",
        )

    # ================================================================
    # Git actions
    # ================================================================

    def open_git_terminal(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open a terminal at the Git repository root."""

        repository_path = self.get_git_root(folder_path) or folder_path

        self.open_interactive_terminal_command(
            folder_path=repository_path,
            setup_command=(
                'echo "Git repository: $(pwd)"; '
                'echo "Branch: $(git branch --show-current 2>/dev/null)"; '
                "echo"
            ),
            title="Git Terminal",
        )

    def git_status(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Show Git status."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command="git status",
            title="Git Status",
        )

    def git_log(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Show a concise decorated Git log."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command=("git --no-pager log --graph --decorate --oneline --all -n 30"),
            title="Git Log",
        )

    def git_fetch(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Fetch from all configured remotes."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command="git fetch --all --prune",
            title="Git Fetch",
        )

    def git_pull(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Pull the current branch using fast-forward only."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command="git pull --ff-only",
            title="Git Pull",
        )

    def git_push(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Push the current branch."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command="git push",
            title="Git Push",
        )

    def show_git_branch(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Show the current branch and repository root."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        self.run_terminal_command(
            folder_path=repository_path,
            command=(
                'echo "Repository: $(pwd)"; '
                'echo "Current branch: $(git branch --show-current)"; '
                "echo; "
                "git status --short --branch"
            ),
            title="Current Git Branch",
        )

    def open_git_root(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the repository root in Nautilus."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        nautilus = self.find_command(["nautilus"])

        if not nautilus:
            self.notify(
                "Nautilus not found",
                "The Nautilus executable could not be found.",
            )
            return

        self.launch_process(
            [nautilus, repository_path],
            repository_path,
            "Nautilus",
        )

    def open_git_remote(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the origin remote repository in the web browser."""

        repository_path = self.get_git_root(folder_path)

        if not repository_path:
            self.notify(
                "Not a Git repository",
                "The selected folder is not inside a Git repository.",
            )
            return

        remote_url = self.get_git_remote_url(repository_path)

        if not remote_url:
            self.notify(
                "Git remote unavailable",
                "No origin remote was found for this repository.",
            )
            return

        web_url = self.convert_git_remote_to_web_url(remote_url)

        if not web_url:
            self.notify(
                "Unsupported Git remote",
                f"Could not convert this remote to a web URL: {remote_url}",
            )
            return

        xdg_open = self.find_command(["xdg-open"])

        if not xdg_open:
            self.notify(
                "Browser launcher unavailable",
                "The xdg-open executable could not be found.",
            )
            return

        self.launch_process(
            [xdg_open, web_url],
            repository_path,
            "Remote Repository",
        )

    # ================================================================
    # Docker actions
    # ================================================================

    def compose_up(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start the Docker Compose project."""

        if not self.find_compose_file(folder_path):
            self.notify(
                "Compose file not found",
                "No Compose file exists in the selected folder.",
            )
            return

        self.run_terminal_command(
            folder_path=folder_path,
            command=("docker compose up -d && echo && docker compose ps"),
            title="Docker Compose Up",
        )

    def compose_down(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Stop the Docker Compose project."""

        if not self.find_compose_file(folder_path):
            self.notify(
                "Compose file not found",
                "No Compose file exists in the selected folder.",
            )
            return

        self.run_terminal_command(
            folder_path=folder_path,
            command="docker compose down",
            title="Docker Compose Down",
        )

    def compose_restart(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Restart the Docker Compose project."""

        if not self.find_compose_file(folder_path):
            self.notify(
                "Compose file not found",
                "No Compose file exists in the selected folder.",
            )
            return

        self.run_terminal_command(
            folder_path=folder_path,
            command=("docker compose restart && echo && docker compose ps"),
            title="Docker Compose Restart",
        )

    def compose_logs(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Follow Docker Compose logs until Ctrl+C is pressed."""

        if not self.find_compose_file(folder_path):
            self.notify(
                "Compose file not found",
                "No Compose file exists in the selected folder.",
            )
            return

        self.open_interactive_terminal_command(
            folder_path=folder_path,
            setup_command=(
                'echo "Following Docker Compose logs."; '
                'echo "Press Ctrl+C to stop following logs."; '
                "echo; "
                "docker compose logs --follow --tail=200"
            ),
            title="Docker Compose Logs",
        )

    def docker_containers(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """List Docker containers."""

        self.run_terminal_command(
            folder_path=folder_path,
            command="docker ps -a",
            title="Docker Containers",
        )

    def docker_images(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """List Docker images."""

        self.run_terminal_command(
            folder_path=folder_path,
            command="docker images",
            title="Docker Images",
        )

    def docker_disk_usage(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Show Docker disk usage."""

        self.run_terminal_command(
            folder_path=folder_path,
            command="docker system df",
            title="Docker Disk Usage",
        )

    # ================================================================
    # AI Workstation actions
    # ================================================================

    def open_web_address(
        self,
        folder_path: str,
        web_address: str,
        application_name: str,
    ) -> None:
        """Open a local AI service or web address."""

        xdg_open = self.find_command(["xdg-open"])

        if not xdg_open:
            self.notify(
                "Browser launcher unavailable",
                "The xdg-open executable could not be found.",
            )
            return

        self.launch_process(
            [xdg_open, web_address],
            folder_path,
            application_name,
        )

    def open_dify(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the locally hosted Dify interface."""

        self.open_web_address(
            folder_path=folder_path,
            web_address="http://localhost",
            application_name="Dify",
        )

    def open_openwebui(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the locally hosted Open WebUI interface."""

        self.open_web_address(
            folder_path=folder_path,
            web_address="http://localhost:3001",
            application_name="Open WebUI",
        )

    def open_bentopdf(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the locally hosted BentoPDF interface."""

        self.open_web_address(
            folder_path=folder_path,
            web_address="http://localhost:3000",
            application_name="BentoPDF",
        )

    def open_ollama_api(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open Ollama's model-list API endpoint."""

        self.open_web_address(
            folder_path=folder_path,
            web_address="http://localhost:11434/api/tags",
            application_name="Ollama API",
        )

    def show_gpu_status(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Display NVIDIA GPU utilization and memory information."""

        if not self.find_command(["nvidia-smi"]):
            self.notify(
                "NVIDIA utility unavailable",
                "The nvidia-smi command could not be found.",
            )
            return

        self.run_terminal_command(
            folder_path=folder_path,
            command="nvidia-smi",
            title="NVIDIA GPU Status",
        )

    def show_cuda_information(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Display driver, CUDA runtime and CUDA toolkit information."""

        command = (
            'echo "================ NVIDIA DRIVER / RUNTIME ================"; '
            "if command -v nvidia-smi >/dev/null 2>&1; then "
            "nvidia-smi; "
            "else "
            'echo "nvidia-smi is not installed."; '
            "fi; "
            "echo; "
            'echo "================ CUDA TOOLKIT ============================"; '
            "if command -v nvcc >/dev/null 2>&1; then "
            "nvcc --version; "
            "else "
            'echo "nvcc is not available on PATH."; '
            'echo "This does not necessarily mean CUDA GPU support is unavailable."; '
            "fi; "
            "echo; "
            'echo "================ PYTORCH CUDA ============================"; '
            "python3 -c "
            '"import torch; '
            "print('PyTorch:', torch.__version__); "
            "print('CUDA available:', torch.cuda.is_available()); "
            "print('PyTorch CUDA build:', torch.version.cuda); "
            "print('GPU count:', torch.cuda.device_count()); "
            "[print(f'GPU {i}: {torch.cuda.get_device_name(i)}') "
            'for i in range(torch.cuda.device_count())]" '
            "2>/dev/null || "
            'echo "PyTorch is not installed in the system Python environment."'
        )

        self.run_terminal_command(
            folder_path=folder_path,
            command=command,
            title="CUDA Information",
        )

    def show_ollama_status(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Check the Ollama service and API."""

        command = (
            'echo "================ OLLAMA EXECUTABLE ======================"; '
            "if command -v ollama >/dev/null 2>&1; then "
            "ollama --version; "
            "else "
            'echo "The ollama executable is not available on PATH."; '
            "fi; "
            "echo; "
            'echo "================ OLLAMA PROCESS ========================="; '
            "pgrep -a ollama || "
            'echo "No Ollama process was found."; '
            "echo; "
            'echo "================ OLLAMA API ============================="; '
            "if command -v curl >/dev/null 2>&1; then "
            "if curl -fsS --max-time 5 "
            "http://localhost:11434/api/tags >/dev/null; then "
            'echo "Ollama API is responding at http://localhost:11434"; '
            "else "
            'echo "Ollama API is not responding."; '
            "fi; "
            "else "
            'echo "curl is not installed; API check skipped."; '
            "fi"
        )

        self.run_terminal_command(
            folder_path=folder_path,
            command=command,
            title="Ollama Service Status",
        )

    def show_ollama_models(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """List locally installed Ollama models."""

        if not self.find_command(["ollama"]):
            self.notify(
                "Ollama unavailable",
                "The ollama executable could not be found.",
            )
            return

        self.run_terminal_command(
            folder_path=folder_path,
            command="ollama list",
            title="Installed Ollama Models",
        )

    def pull_ollama_model(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Prompt for an Ollama model name and download it."""

        ollama = self.find_command(["ollama"])
        zenity = self.find_command(["zenity"])

        if not ollama:
            self.notify(
                "Ollama unavailable",
                "The ollama executable could not be found.",
            )
            return

        if not zenity:
            self.notify(
                "Zenity unavailable",
                "Install Zenity to use the model-name dialog.",
            )
            return

        try:
            result = subprocess.run(
                [
                    zenity,
                    "--entry",
                    "--title=Pull Ollama Model",
                    "--text=Enter the Ollama model name:",
                    "--entry-text=",
                    "--width=520",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return

            model_name = result.stdout.strip()

            if not model_name:
                return

            if any(character.isspace() for character in model_name):
                self.notify(
                    "Invalid model name",
                    "The model name must not contain spaces.",
                )
                return

            allowed_characters = set(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/:"
            )

            if any(character not in allowed_characters for character in model_name):
                self.notify(
                    "Invalid model name",
                    "The model name contains unsupported characters.",
                )
                return

            quoted_model_name = shlex.quote(model_name)

            self.run_terminal_command(
                folder_path=folder_path,
                command=f"ollama pull {quoted_model_name}",
                title=f"Ollama Pull: {model_name}",
            )

        except Exception as error:
            self.notify(
                "Ollama model pull error",
                str(error),
            )

    # ================================================================
    # Smart project detection and actions
    # ================================================================

    def detect_project_root(self, folder_path: str) -> str:
        """Return the most likely project root."""

        git_root = self.get_git_root(folder_path)

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

    def detect_project(self, folder_path: str) -> dict:
        """Inspect the selected folder and identify project capabilities."""

        root = Path(self.detect_project_root(folder_path)).expanduser().resolve()

        project = {
            "root": str(root),
            "git": self.get_git_root(str(root)) is not None,
            "python": False,
            "environment_file": None,
            "local_environment": None,
            "requirements": None,
            "pyproject": None,
            "jupyter": False,
            "streamlit": False,
            "streamlit_entry": None,
            "fastapi": False,
            "fastapi_entry": None,
            "docker": False,
            "compose_file": None,
            "dockerfile": None,
            "modelfile": None,
        }

        for name in ["environment.yml", "environment.yaml"]:
            candidate = root / name

            if candidate.is_file():
                project["environment_file"] = str(candidate)
                project["python"] = True
                break

        for name in [".venv", "venv"]:
            candidate = root / name

            if candidate.is_dir() and (candidate / "bin" / "python").is_file():
                project["local_environment"] = str(candidate)
                project["python"] = True
                break

        requirements = root / "requirements.txt"

        if requirements.is_file():
            project["requirements"] = str(requirements)
            project["python"] = True

        pyproject = root / "pyproject.toml"

        if pyproject.is_file():
            project["pyproject"] = str(pyproject)
            project["python"] = True

        compose_file = self.find_compose_file(str(root))

        if compose_file:
            project["compose_file"] = compose_file
            project["docker"] = True

        dockerfile = root / "Dockerfile"

        if dockerfile.is_file():
            project["dockerfile"] = str(dockerfile)
            project["docker"] = True

        modelfile = root / "Modelfile"

        if modelfile.is_file():
            project["modelfile"] = str(modelfile)

        try:
            project["jupyter"] = any(root.rglob("*.ipynb"))
        except Exception:
            project["jupyter"] = False

        if project["jupyter"]:
            project["python"] = True

        python_files = find_python_files(root)

        preferred_streamlit_names = [
            "streamlit_app.py",
            "app.py",
            "main.py",
        ]

        ordered_streamlit_files = sorted(
            python_files,
            key=lambda path: (
                path.name not in preferred_streamlit_names,
                len(path.parts),
                str(path),
            ),
        )

        for python_file in ordered_streamlit_files:
            if file_contains_any(
                python_file,
                [
                    "import streamlit",
                    "from streamlit",
                    "st.set_page_config",
                    "st.title(",
                ],
            ):
                project["streamlit"] = True
                project["streamlit_entry"] = str(python_file)
                project["python"] = True
                break

        preferred_fastapi_paths = [
            root / "api" / "main.py",
            root / "app" / "main.py",
            root / "main.py",
            root / "src" / "main.py",
        ]

        ordered_fastapi_files = [path for path in preferred_fastapi_paths if path.is_file()]

        ordered_fastapi_files.extend(
            path for path in python_files if path not in ordered_fastapi_files
        )

        for python_file in ordered_fastapi_files:
            if file_contains_any(
                python_file,
                [
                    "from fastapi import",
                    "import fastapi",
                    "fastapi(",
                ],
            ):
                project["fastapi"] = True
                project["fastapi_entry"] = str(python_file)
                project["python"] = True
                break

        return project

    def project_report(self, project: dict) -> str:
        """Build a readable project-detection report."""

        def yes_no(value: object) -> str:
            return "Yes" if value else "No"

        lines = [
            f"Project root: {project['root']}",
            "",
            "Detected capabilities",
            f"Git repository: {yes_no(project['git'])}",
            f"Python project: {yes_no(project['python'])}",
            f"Jupyter notebooks: {yes_no(project['jupyter'])}",
            f"Streamlit application: {yes_no(project['streamlit'])}",
            f"FastAPI application: {yes_no(project['fastapi'])}",
            f"Docker project: {yes_no(project['docker'])}",
            f"Ollama Modelfile: {yes_no(project['modelfile'])}",
            "",
            "Detected details",
        ]

        details = [
            ("Environment file", "environment_file"),
            ("Local environment", "local_environment"),
            ("Requirements", "requirements"),
            ("pyproject.toml", "pyproject"),
            ("Streamlit entry", "streamlit_entry"),
            ("FastAPI entry", "fastapi_entry"),
            ("Compose file", "compose_file"),
            ("Dockerfile", "dockerfile"),
            ("Modelfile", "modelfile"),
        ]

        found = False

        for label, key in details:
            value = project.get(key)

            if value:
                lines.append(f"{label}: {value}")
                found = True

        if not found:
            lines.append("No recognized project files were found.")

        return "\n".join(lines)

    def show_detected_project(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Show project detection results."""

        project = self.detect_project(folder_path)
        report = self.project_report(project)
        zenity = self.find_command(["zenity"])

        if zenity:
            process = subprocess.Popen(
                [
                    zenity,
                    "--text-info",
                    "--title=Detected Project",
                    "--width=820",
                    "--height=620",
                ],
                stdin=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )

            process.communicate(report)
            return

        self.run_terminal_command(
            folder_path=project["root"],
            command=f"printf '%s\\n' {shlex.quote(report)}",
            title="Detected Project",
        )

    def open_project_terminal(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open a terminal at the detected project root."""

        project = self.detect_project(folder_path)

        self.open_interactive_terminal_command(
            folder_path=project["root"],
            setup_command='echo "Project root: $(pwd)"; echo',
            title="Project Terminal",
        )

    def open_detected_environment(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Activate a detected local or Conda environment."""

        project = self.detect_project(folder_path)
        local_environment = project.get("local_environment")

        if local_environment:
            activate = Path(local_environment) / "bin" / "activate"

            self.open_interactive_terminal_command(
                folder_path=project["root"],
                setup_command=(
                    f"source {shlex.quote(str(activate))}; "
                    'echo "Activated: $VIRTUAL_ENV"; '
                    'echo "Python: $(command -v python)"; echo'
                ),
                title="Detected Python Environment",
            )
            return

        environment_file = project.get("environment_file")

        if environment_file:
            environment_name = None

            try:
                for line in (
                    Path(environment_file)
                    .read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                    .splitlines()
                ):
                    if line.strip().startswith("name:"):
                        environment_name = line.split(":", 1)[1].strip()
                        break
            except Exception:
                environment_name = None

            if environment_name:
                for name, path in self.get_conda_environments():
                    if name == environment_name:
                        self.open_conda_terminal(
                            environment_path=path,
                            folder_path=project["root"],
                        )
                        return

            self.notify(
                "Conda environment not matched",
                "Choose the environment manually.",
            )

            self.select_and_launch_conda_tool(folder_path=project["root"])
            return

        self.notify(
            "No environment detected",
            "No .venv, venv, environment.yml or environment.yaml was found.",
        )

    def run_project_command(
        self,
        project: dict,
        command: str,
        title: str,
    ) -> None:
        """Run a project command using a local virtual environment when found."""

        local_environment = project.get("local_environment")

        if local_environment:
            activate = Path(local_environment) / "bin" / "activate"
            command = f"source {shlex.quote(str(activate))}; {command}"

        self.open_interactive_terminal_command(
            folder_path=project["root"],
            setup_command=command,
            title=title,
        )

    def start_project_jupyterlab(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start JupyterLab at the detected project root."""

        project = self.detect_project(folder_path)

        self.run_project_command(
            project,
            (
                "if command -v jupyter-lab >/dev/null 2>&1; "
                "then jupyter-lab; "
                "else echo 'JupyterLab is not installed in this environment.'; "
                "fi"
            ),
            "Project JupyterLab",
        )

    def run_detected_streamlit(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Run the detected Streamlit application."""

        project = self.detect_project(folder_path)
        entry = project.get("streamlit_entry")

        if not entry:
            self.notify(
                "Streamlit entry not found",
                "No Streamlit application was detected.",
            )
            return

        relative_entry = str(Path(entry).relative_to(Path(project["root"])))

        self.run_project_command(
            project,
            (
                "if command -v streamlit >/dev/null 2>&1; "
                f"then streamlit run {shlex.quote(relative_entry)}; "
                "else echo 'Streamlit is not installed in this environment.'; "
                "fi"
            ),
            "Streamlit Application",
        )

    def run_detected_fastapi(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Run the detected FastAPI application."""

        project = self.detect_project(folder_path)
        entry = project.get("fastapi_entry")

        if not entry:
            self.notify(
                "FastAPI entry not found",
                "No FastAPI application was detected.",
            )
            return

        module_name = module_name_from_file(
            project["root"],
            entry,
        )

        self.run_project_command(
            project,
            (
                "if command -v uvicorn >/dev/null 2>&1; "
                f"then uvicorn {shlex.quote(module_name)}:app --reload; "
                "else echo 'Uvicorn is not installed in this environment.'; "
                "fi"
            ),
            "FastAPI Application",
        )

    def open_fastapi_documentation(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the conventional local FastAPI Swagger UI."""

        self.open_web_address(
            folder_path=folder_path,
            web_address="http://localhost:8000/docs",
            application_name="FastAPI Documentation",
        )

    def project_compose_up(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Start Compose from the detected project root."""

        project = self.detect_project(folder_path)

        self.run_terminal_command(
            folder_path=project["root"],
            command="docker compose up -d && echo && docker compose ps",
            title="Project Compose Up",
        )

    def project_compose_down(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Stop Compose from the detected project root."""

        project = self.detect_project(folder_path)

        self.run_terminal_command(
            folder_path=project["root"],
            command="docker compose down",
            title="Project Compose Down",
        )

    def build_detected_ollama_model(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Build an Ollama model from a detected Modelfile."""

        project = self.detect_project(folder_path)
        zenity = self.find_command(["zenity"])

        if not project.get("modelfile"):
            self.notify("Modelfile not found", "No Modelfile was detected.")
            return

        if not zenity:
            self.notify("Zenity unavailable", "Zenity is required.")
            return

        result = subprocess.run(
            [
                zenity,
                "--entry",
                "--title=Build Ollama Model",
                "--text=Enter the model name:",
                "--width=520",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return

        model_name = result.stdout.strip()

        if not model_name:
            return

        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/:")

        if any(character not in allowed for character in model_name):
            self.notify(
                "Invalid model name",
                "Use letters, numbers, dots, underscores, hyphens, slashes and colons.",
            )
            return

        self.run_terminal_command(
            folder_path=project["root"],
            command=(f"ollama create {shlex.quote(model_name)} -f Modelfile"),
            title=f"Build Ollama Model: {model_name}",
        )

    # ================================================================
    # New project wizard
    # ================================================================

    def create_project_template(
        self,
        parent_folder: str,
        project_name: str,
        template_name: str,
        initialize_git: bool,
    ) -> str:
        """Create a selected project skeleton."""

        project_root = Path(parent_folder).expanduser().resolve() / project_name

        if project_root.exists():
            raise FileExistsError(f"Destination already exists: {project_root}")

        project_root.mkdir(parents=True)
        package_name = project_name.replace("-", "_").replace(".", "_")

        gitignore = (
            "__pycache__/\n"
            "*.py[cod]\n"
            ".pytest_cache/\n"
            ".mypy_cache/\n"
            ".ruff_cache/\n"
            ".venv/\n"
            "venv/\n"
            ".env\n"
            ".ipynb_checkpoints/\n"
            ".vscode/\n"
            ".idea/\n"
            ".DS_Store\n"
            "data/raw/\n"
            "data/processed/\n"
            "models/\n"
            "outputs/\n"
            "*.pt\n"
            "*.pth\n"
            "*.ckpt\n"
        )

        title = project_name.replace("_", " ").replace("-", " ").title()

        write_new_file(project_root / ".gitignore", gitignore)

        if template_name == "Basic Python":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nPython project.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                "",
            )
            write_new_file(
                project_root / "src" / package_name / "__init__.py",
                "",
            )
            write_new_file(
                project_root / "src" / package_name / "main.py",
                (
                    "def main() -> None:\n"
                    '    """Application entry point."""\n'
                    '    print("Project is ready.")\n\n\n'
                    'if __name__ == "__main__":\n'
                    "    main()\n"
                ),
            )
            write_new_file(
                project_root / "tests" / "test_smoke.py",
                "def test_smoke() -> None:\n    assert True\n",
            )

        elif template_name == "Data Science":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nData-science project.\n",
            )
            write_new_file(
                project_root / "environment.yml",
                (
                    f"name: {package_name}\n"
                    "channels:\n"
                    "  - conda-forge\n"
                    "dependencies:\n"
                    "  - python=3.11\n"
                    "  - numpy\n"
                    "  - pandas\n"
                    "  - matplotlib\n"
                    "  - scikit-learn\n"
                    "  - jupyterlab\n"
                    "  - ipykernel\n"
                ),
            )

            for directory_name in [
                "data/raw",
                "data/processed",
                "notebooks",
                "src",
                "models",
                "outputs",
                "reports/figures",
                "tests",
            ]:
                write_new_file(
                    project_root / directory_name / ".gitkeep",
                    "",
                )

        elif template_name == "Streamlit":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nStreamlit application.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                "streamlit\n",
            )
            write_new_file(
                project_root / "app.py",
                (
                    "import streamlit as st\n\n\n"
                    "st.set_page_config(\n"
                    '    page_title="Streamlit Application",\n'
                    '    layout="wide",\n'
                    ")\n\n"
                    'st.title("Streamlit Application")\n'
                    'st.write("Project is ready.")\n'
                ),
            )
            write_new_file(
                project_root / ".streamlit" / "config.toml",
                "[server]\nheadless = true\n",
            )

        elif template_name == "FastAPI":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nFastAPI application.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                "fastapi\nuvicorn[standard]\n",
            )
            write_new_file(
                project_root / "app" / "__init__.py",
                "",
            )
            write_new_file(
                project_root / "app" / "main.py",
                (
                    "from fastapi import FastAPI\n\n\n"
                    'app = FastAPI(title="FastAPI Application")\n\n\n'
                    '@app.get("/health")\n'
                    "def health() -> dict[str, str]:\n"
                    '    """Return service health."""\n'
                    '    return {"status": "ok"}\n'
                ),
            )

        elif template_name == "Docker Compose":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nDocker Compose project.\n",
            )
            write_new_file(
                project_root / "compose.yml",
                ('services:\n  app:\n    build: .\n    ports:\n      - "8000:8000"\n'),
            )
            write_new_file(
                project_root / "Dockerfile",
                (
                    "FROM python:3.11-slim\n\n"
                    "WORKDIR /app\n"
                    "COPY requirements.txt .\n"
                    "RUN pip install --no-cache-dir -r requirements.txt\n"
                    "COPY . .\n"
                    'CMD ["python", "app.py"]\n'
                ),
            )
            write_new_file(
                project_root / "requirements.txt",
                "",
            )
            write_new_file(
                project_root / "app.py",
                'print("Docker project is ready.")\n',
            )

        elif template_name == "RAG Application":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nLocal retrieval-augmented generation project.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                ("langchain\nlangchain-community\nchromadb\npypdf\nollama\n"),
            )

            for directory_name in [
                "data/documents",
                "data/vector_store",
                "src",
                "tests",
                "config",
            ]:
                write_new_file(
                    project_root / directory_name / ".gitkeep",
                    "",
                )

            write_new_file(
                project_root / "src" / "main.py",
                (
                    "def main() -> None:\n"
                    '    """Run the RAG application."""\n'
                    '    print("RAG project skeleton is ready.")\n\n\n'
                    'if __name__ == "__main__":\n'
                    "    main()\n"
                ),
            )

        elif template_name == "Agent Application":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nAgentic AI application.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                "pydantic\nhttpx\nollama\n",
            )

            for directory_name in [
                "src/agents",
                "src/tools",
                "src/workflows",
                "tests",
                "config",
            ]:
                write_new_file(
                    project_root / directory_name / ".gitkeep",
                    "",
                )

            write_new_file(
                project_root / "src" / "main.py",
                (
                    "def main() -> None:\n"
                    '    """Run the agent application."""\n'
                    '    print("Agent project skeleton is ready.")\n\n\n'
                    'if __name__ == "__main__":\n'
                    "    main()\n"
                ),
            )

        elif template_name == "MCP Server":
            write_new_file(
                project_root / "README.md",
                f"# {title}\n\nModel Context Protocol server.\n",
            )
            write_new_file(
                project_root / "requirements.txt",
                "mcp\n",
            )
            write_new_file(
                project_root / "server.py",
                (
                    "from mcp.server.fastmcp import FastMCP\n\n\n"
                    'mcp = FastMCP("Local MCP Server")\n\n\n'
                    "@mcp.tool()\n"
                    "def hello(name: str) -> str:\n"
                    '    """Return a greeting."""\n'
                    '    return f"Hello, {name}!"\n\n\n'
                    'if __name__ == "__main__":\n'
                    "    mcp.run()\n"
                ),
            )

        else:
            raise ValueError(f"Unsupported template: {template_name}")

        if initialize_git:
            git = self.find_command(["git"])

            if git:
                subprocess.run(
                    [git, "init"],
                    cwd=str(project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                    timeout=15,
                )

        return str(project_root)

    def choose_environment_setup(
        self,
        template_name: str,
    ) -> str | None:
        """Ask how the new project's Python environment should be created."""

        python_templates = {
            "Basic Python",
            "Data Science",
            "Streamlit",
            "FastAPI",
            "RAG Application",
            "Agent Application",
            "MCP Server",
        }

        if template_name not in python_templates:
            return "None"

        zenity = self.find_command(["zenity"])

        if not zenity:
            return "None"

        options = [
            "None",
            "Python .venv",
            "Conda environment",
        ]

        command = [
            zenity,
            "--list",
            "--radiolist",
            "--title=New Project Wizard",
            "--text=Choose environment setup:",
            "--width=620",
            "--height=360",
            "--column=Select",
            "--column=Environment",
        ]

        for index, option in enumerate(options):
            command.extend(
                [
                    "TRUE" if index == 0 else "FALSE",
                    option,
                ]
            )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip() or "None"

    def choose_post_creation_actions(
        self,
        template_name: str,
        environment_setup: str,
    ) -> list[str] | None:
        """Ask which optional actions should run after project creation."""

        zenity = self.find_command(["zenity"])

        if not zenity:
            return []

        rows = [
            (
                "Install dependencies",
                template_name != "Basic Python",
            ),
            (
                "Open in VSCodium",
                self.find_command(["codium", "codium-insiders", "vscodium"]) is not None,
            ),
            (
                "Open project terminal",
                True,
            ),
            (
                "Launch application",
                template_name in {"Streamlit", "FastAPI"},
            ),
        ]

        command = [
            zenity,
            "--list",
            "--checklist",
            "--title=New Project Wizard",
            "--text=Choose optional post-creation actions:",
            "--width=680",
            "--height=430",
            "--separator=|",
            "--column=Select",
            "--column=Action",
        ]

        for label, default_selected in rows:
            command.extend(
                [
                    "TRUE" if default_selected else "FALSE",
                    label,
                ]
            )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        output = result.stdout.strip()

        if not output:
            return []

        return [item.strip() for item in output.split("|") if item.strip()]

    @staticmethod
    def read_conda_environment_name(
        environment_file: Path,
    ) -> str | None:
        """Read the environment name from environment.yml."""

        try:
            for line in environment_file.read_text(
                encoding="utf-8",
                errors="ignore",
            ).splitlines():
                stripped = line.strip()

                if stripped.startswith("name:"):
                    value = stripped.split(":", 1)[1].strip()

                    if value:
                        return value
        except Exception:
            return None

        return None

    def create_project_environment(
        self,
        project_root: str,
        template_name: str,
        environment_setup: str,
        install_dependencies: bool,
    ) -> str | None:
        """Create the selected environment and optionally install dependencies."""

        root = Path(project_root)
        terminal = self.find_command(["gnome-terminal"])

        if not terminal or environment_setup == "None":
            return None

        if environment_setup == "Python .venv":
            requirements = root / "requirements.txt"

            commands = [
                "python3 -m venv .venv",
                "source .venv/bin/activate",
                "python -m pip install --upgrade pip",
            ]

            if install_dependencies and requirements.is_file():
                commands.append("python -m pip install -r requirements.txt")

            commands.extend(
                [
                    "echo",
                    'echo "Virtual environment setup completed."',
                    'echo "Environment: $(pwd)/.venv"',
                    "echo",
                    'echo "Press Enter to close this terminal."',
                    "read -r",
                ]
            )

            self.launch_process(
                [
                    terminal,
                    "--working-directory",
                    project_root,
                    "--",
                    "bash",
                    "-lc",
                    "; ".join(commands),
                ],
                project_root,
                "Create Python Environment",
            )

            return ".venv"

        if environment_setup == "Conda environment":
            conda = self.find_conda_executable()

            if not conda:
                self.notify(
                    "Conda unavailable",
                    "Conda could not be found. The project was still created.",
                )
                return None

            conda_root = Path(conda).parent.parent
            conda_script = conda_root / "etc" / "profile.d" / "conda.sh"
            environment_file = root / "environment.yml"

            if environment_file.is_file():
                environment_name = self.read_conda_environment_name(environment_file)

                commands = [
                    f"source {shlex.quote(str(conda_script))}",
                    (f"conda env create -f {shlex.quote(str(environment_file))}"),
                ]

                if environment_name:
                    commands.append(f"conda activate {shlex.quote(environment_name)}")

                    requirements = root / "requirements.txt"

                    if install_dependencies and requirements.is_file():
                        commands.append("python -m pip install -r requirements.txt")

                commands.extend(
                    [
                        "echo",
                        'echo "Conda environment setup completed."',
                        "echo",
                        'echo "Press Enter to close this terminal."',
                        "read -r",
                    ]
                )

                self.launch_process(
                    [
                        terminal,
                        "--working-directory",
                        project_root,
                        "--",
                        "bash",
                        "-lc",
                        "; ".join(commands),
                    ],
                    project_root,
                    "Create Conda Environment",
                )

                return environment_name or "environment.yml"

            environment_name = root.name.replace("-", "_").replace(".", "_")

            commands = [
                f"source {shlex.quote(str(conda_script))}",
                (f"conda create -y -n {shlex.quote(environment_name)} python=3.11 pip"),
                f"conda activate {shlex.quote(environment_name)}",
                "python -m pip install --upgrade pip",
            ]

            requirements = root / "requirements.txt"

            if install_dependencies and requirements.is_file():
                commands.append("python -m pip install -r requirements.txt")

            commands.extend(
                [
                    "echo",
                    'echo "Conda environment setup completed."',
                    f'echo "Environment: {environment_name}"',
                    "echo",
                    'echo "Press Enter to close this terminal."',
                    "read -r",
                ]
            )

            self.launch_process(
                [
                    terminal,
                    "--working-directory",
                    project_root,
                    "--",
                    "bash",
                    "-lc",
                    "; ".join(commands),
                ],
                project_root,
                "Create Conda Environment",
            )

            return environment_name

        return None

    def run_sequential_project_setup(
        self,
        project_root: str,
        template_name: str,
        environment_setup: str,
        install_dependencies: bool,
        launch_application: bool,
        open_vscodium: bool,
        open_project_terminal: bool,
    ) -> None:
        """Run environment setup, installation and app launch sequentially."""

        terminal = self.find_command(["gnome-terminal"])

        if not terminal:
            self.notify(
                "Terminal unavailable",
                "GNOME Terminal could not be found.",
            )
            return

        root = Path(project_root)
        requirements = root / "requirements.txt"
        commands = [
            (
                "set -Ee; "
                "trap 'status=$?; echo; "
                'echo "Wizard v3.1.1 failed with exit code $status."; '
                'echo "Press Enter to close this terminal."; '
                "read -r; exit $status' ERR"
            ),
            f"cd {shlex.quote(project_root)}",
            'echo "=== New Project Wizard v3.1 ==="',
            'echo "Project: $(pwd)"',
            "echo",
        ]

        if environment_setup == "Python .venv":
            commands.extend(
                [
                    'echo "[1/4] Creating Python virtual environment..."',
                    "python3 -m venv .venv",
                    "source .venv/bin/activate",
                    "python -m pip install --upgrade pip",
                ]
            )

            if install_dependencies and requirements.is_file():
                commands.extend(
                    [
                        'echo "[2/4] Installing dependencies..."',
                        "python -m pip install -r requirements.txt",
                    ]
                )
            else:
                commands.append('echo "[2/4] Dependency installation skipped."')

        elif environment_setup == "Conda environment":
            conda = self.find_conda_executable()

            if not conda:
                self.notify(
                    "Conda unavailable",
                    "Conda could not be found. The project was created only.",
                )
                return

            conda_root = Path(conda).parent.parent
            conda_script = conda_root / "etc" / "profile.d" / "conda.sh"
            environment_file = root / "environment.yml"

            commands.extend(
                [
                    f"source {shlex.quote(str(conda_script))}",
                    'echo "[1/4] Creating Conda environment..."',
                ]
            )

            if environment_file.is_file():
                environment_name = self.read_conda_environment_name(environment_file)

                if not environment_name:
                    environment_name = root.name.replace("-", "_").replace(".", "_")

                commands.extend(
                    [
                        (
                            f"if conda env list | awk '{{print $1}}' | "
                            f"grep -Fxq {shlex.quote(environment_name)}; then "
                            f"echo 'Conda environment already exists: "
                            f"{environment_name}'; "
                            f"else conda env create -f "
                            f"{shlex.quote(str(environment_file))}; fi"
                        ),
                        f"conda activate {shlex.quote(environment_name)}",
                    ]
                )
            else:
                environment_name = root.name.replace("-", "_").replace(".", "_")

                commands.extend(
                    [
                        (
                            f"if conda env list | awk '{{print $1}}' | "
                            f"grep -Fxq {shlex.quote(environment_name)}; then "
                            f"echo 'Conda environment already exists: "
                            f"{environment_name}'; "
                            f"else conda create -y -n "
                            f"{shlex.quote(environment_name)} python=3.11 pip; fi"
                        ),
                        f"conda activate {shlex.quote(environment_name)}",
                        "python -m pip install --upgrade pip",
                    ]
                )

            if install_dependencies and requirements.is_file():
                commands.extend(
                    [
                        'echo "[2/4] Installing dependencies..."',
                        "python -m pip install -r requirements.txt",
                    ]
                )
            else:
                commands.append('echo "[2/4] Dependency installation skipped."')

        else:
            commands.extend(
                [
                    'echo "[1/4] Environment creation skipped."',
                    'echo "[2/4] Dependency installation skipped."',
                ]
            )

        if launch_application and template_name in {"Streamlit", "FastAPI"}:
            if template_name == "Streamlit":
                app_command = (
                    "streamlit run app.py --server.headless true --server.address 127.0.0.1"
                )
                port = 8501
                url = "http://localhost:8501"
            else:
                app_command = "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
                port = 8000
                url = "http://localhost:8000/docs"

            commands.extend(
                [
                    'echo "[3/4] Starting application..."',
                    f"{app_command} & APP_PID=$!",
                    (
                        f"for attempt in $(seq 1 60); do "
                        f"if curl -fsS --max-time 1 "
                        f"http://127.0.0.1:{port} >/dev/null 2>&1; then "
                        f"break; fi; "
                        f"if ! kill -0 $APP_PID 2>/dev/null; then "
                        f"echo 'Application process stopped unexpectedly.'; "
                        f"wait $APP_PID; exit 1; fi; "
                        f"sleep 1; "
                        f"done"
                    ),
                    (
                        f"if ! curl -fsS --max-time 2 "
                        f"http://127.0.0.1:{port} >/dev/null 2>&1; then "
                        f"echo 'Application did not become ready within 60 seconds.'; "
                        f"kill $APP_PID 2>/dev/null || true; exit 1; fi"
                    ),
                    'echo "[4/4] Application is responding."',
                    f"xdg-open {shlex.quote(url)} >/dev/null 2>&1 || true",
                ]
            )

            if open_vscodium:
                commands.append("nohup codium . >/dev/null 2>&1 </dev/null & disown")

            if open_project_terminal:
                commands.append(
                    'nohup gnome-terminal --working-directory="$PWD" >/dev/null 2>&1 </dev/null & disown'
                )

            commands.extend(
                [
                    "echo",
                    f"echo 'Application URL: {url}'",
                    'echo "Keep this terminal open while the application is running."',
                    'echo "Press Ctrl+C to stop the application."',
                    "wait $APP_PID",
                ]
            )

        else:
            commands.extend(
                [
                    'echo "[3/4] Application launch skipped."',
                    'echo "[4/4] Setup completed."',
                ]
            )

            if open_vscodium:
                commands.append("nohup codium . >/dev/null 2>&1 </dev/null & disown")

            if open_project_terminal:
                commands.append(
                    'nohup gnome-terminal --working-directory="$PWD" >/dev/null 2>&1 </dev/null & disown'
                )

            commands.extend(
                [
                    "echo",
                    'echo "Project setup completed successfully."',
                    'echo "Press Enter to close this terminal."',
                    "read -r",
                ]
            )

        shell_command = "; ".join(commands)

        self.launch_process(
            [
                terminal,
                "--working-directory",
                project_root,
                "--",
                "bash",
                "-lc",
                shell_command,
            ],
            project_root,
            "New Project Wizard v3.1",
        )

    def open_new_project_in_vscodium(
        self,
        project_root: str,
    ) -> None:
        """Open the newly created project in VSCodium."""

        command = self.find_command(["codium", "codium-insiders", "vscodium"])

        if not command:
            self.notify(
                "VSCodium unavailable",
                "The project was created, but VSCodium was not found.",
            )
            return

        self.launch_process(
            [command, project_root],
            project_root,
            "VSCodium",
        )

    def launch_new_project_application(
        self,
        project_root: str,
        template_name: str,
        environment_setup: str,
    ) -> None:
        """Launch a newly created Streamlit or FastAPI project."""

        if template_name == "Streamlit":
            command = "streamlit run app.py"
            title = "New Streamlit Application"
        elif template_name == "FastAPI":
            command = "uvicorn app.main:app --reload"
            title = "New FastAPI Application"
        else:
            return

        if environment_setup == "Python .venv":
            command = (
                "while [ ! -f .venv/bin/activate ]; do sleep 1; done; "
                "source .venv/bin/activate; "
                f"{command}"
            )
        elif environment_setup == "Conda environment":
            conda = self.find_conda_executable()

            if conda:
                conda_root = Path(conda).parent.parent
                conda_script = conda_root / "etc" / "profile.d" / "conda.sh"
                environment_file = Path(project_root) / "environment.yml"
                environment_name = None

                if environment_file.is_file():
                    environment_name = self.read_conda_environment_name(environment_file)

                if not environment_name:
                    environment_name = Path(project_root).name.replace("-", "_").replace(".", "_")

                command = (
                    f"source {shlex.quote(str(conda_script))}; "
                    f"while ! conda env list | awk '{{print $1}}' | "
                    f"grep -Fxq {shlex.quote(environment_name)}; "
                    "do sleep 2; done; "
                    f"conda activate {shlex.quote(environment_name)}; "
                    f"{command}"
                )

        self.open_interactive_terminal_command(
            folder_path=project_root,
            setup_command=command,
            title=title,
        )

    def new_project_wizard(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open the graphical New Project Wizard v3.1."""

        zenity = self.find_command(["zenity"])

        if not zenity:
            self.notify(
                "Zenity unavailable",
                "Install Zenity to use the project wizard.",
            )
            return

        templates = [
            "Basic Python",
            "Data Science",
            "Streamlit",
            "FastAPI",
            "Docker Compose",
            "RAG Application",
            "Agent Application",
            "MCP Server",
        ]

        command = [
            zenity,
            "--list",
            "--radiolist",
            "--title=New Project Wizard v3.1",
            "--text=Choose a project type:",
            "--width=620",
            "--height=520",
            "--column=Select",
            "--column=Project type",
        ]

        for index, template in enumerate(templates):
            command.extend(
                [
                    "TRUE" if index == 0 else "FALSE",
                    template,
                ]
            )

        template_result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if template_result.returncode != 0:
            return

        template_name = template_result.stdout.strip()

        if not template_name:
            return

        name_result = subprocess.run(
            [
                zenity,
                "--entry",
                "--title=New Project Wizard v3.1",
                "--text=Enter the new project folder name:",
                "--width=520",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if name_result.returncode != 0:
            return

        project_name = name_result.stdout.strip()

        if not project_name:
            return

        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")

        if project_name in {".", ".."} or any(
            character not in allowed for character in project_name
        ):
            self.notify(
                "Invalid project name",
                "Use letters, numbers, dots, underscores and hyphens only.",
            )
            return

        git_result = subprocess.run(
            [
                zenity,
                "--question",
                "--title=New Project Wizard v3.1",
                "--text=Initialize a Git repository?",
                "--ok-label=Initialize Git",
                "--cancel-label=Do Not Initialize",
                "--width=460",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        environment_setup = self.choose_environment_setup(template_name)

        if environment_setup is None:
            return

        post_actions = self.choose_post_creation_actions(
            template_name=template_name,
            environment_setup=environment_setup,
        )

        if post_actions is None:
            return

        try:
            project_root = self.create_project_template(
                parent_folder=folder_path,
                project_name=project_name,
                template_name=template_name,
                initialize_git=git_result.returncode == 0,
            )
        except Exception as error:
            self.notify("Project creation failed", str(error))
            return

        install_dependencies = "Install dependencies" in post_actions

        subprocess.run(
            [
                zenity,
                "--info",
                "--title=Project Created",
                "--text=Project files were created successfully.\n"
                "Wizard v3.1 will now complete setup sequentially:\n\n" + project_root,
                "--width=600",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        self.run_sequential_project_setup(
            project_root=project_root,
            template_name=template_name,
            environment_setup=environment_setup,
            install_dependencies=install_dependencies,
            launch_application="Launch application" in post_actions,
            open_vscodium="Open in VSCodium" in post_actions,
            open_project_terminal="Open project terminal" in post_actions,
        )

        nautilus = self.find_command(["nautilus"])

        if nautilus:
            self.launch_process(
                [nautilus, project_root],
                project_root,
                "New Project",
            )

    # ================================================================
    # Utility actions
    # ================================================================

    def open_terminal(
        self,
        menu_item: Nautilus.MenuItem,
        folder_path: str,
    ) -> None:
        """Open GNOME Terminal in the selected folder."""

        command = self.find_command(["gnome-terminal"])

        if not command:
            self.notify(
                "Terminal not found",
                "The gnome-terminal executable could not be found.",
            )
            return

        self.launch_process(
            [
                command,
                "--working-directory",
                folder_path,
            ],
            folder_path,
            "GNOME Terminal",
        )

    # ================================================================
    # Editors submenu
    # ================================================================

    def create_editors_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the Editors submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Editors",
            label="Editors",
            tip="Open this folder in an editor",
            icon="accessories-text-editor-symbolic",
        )

        submenu = Nautilus.Menu()

        if self.find_command(["gedit"]):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenGedit",
                label="Open gedit Here",
                tip="Launch gedit from this folder",
                icon="org.gnome.gedit",
            )
            item.connect("activate", self.open_gedit, folder_path)
            submenu.append_item(item)

        if self.find_command(["codium", "codium-insiders", "vscodium"]):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenVSCodium",
                label="Open VSCodium Here",
                tip="Open this folder in VSCodium",
                icon="vscodium",
            )
            item.connect("activate", self.open_vscodium, folder_path)
            submenu.append_item(item)

        if self.find_command(["code", "code-insiders"]):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenVSCode",
                label="Open VS Code Here",
                tip="Open this folder in Visual Studio Code",
                icon="com.visualstudio.code",
            )
            item.connect("activate", self.open_vscode, folder_path)
            submenu.append_item(item)

        if self.find_command(["cursor"]):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenCursor",
                label="Open Cursor Here",
                tip="Open this folder in Cursor",
                icon="cursor",
            )
            item.connect("activate", self.open_cursor, folder_path)
            submenu.append_item(item)

        if self.find_command(
            [
                "pycharm",
                "pycharm-professional",
                "pycharm-community",
                "pycharm.sh",
            ]
        ):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenPyCharm",
                label="Open PyCharm Here",
                tip="Open this folder in PyCharm",
                icon="pycharm",
            )
            item.connect("activate", self.open_pycharm, folder_path)
            submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # Python submenu
    # ================================================================

    def create_python_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the Conda-aware Python submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Python",
            label="Python",
            tip="Conda-aware Python and Jupyter tools",
            icon="text-x-python-symbolic",
        )

        submenu = Nautilus.Menu()

        items = [
            (
                "OpenCondaShell",
                "Open Conda Shell Here",
                "Choose a Conda environment and open a shell",
                self.open_conda_shell,
                "utilities-terminal-symbolic",
            ),
            (
                "StartPythonREPL",
                "Start Python REPL",
                "Choose a Conda environment and start Python",
                self.start_python_repl,
                "text-x-python-symbolic",
            ),
            (
                "StartIPython",
                "Start IPython",
                "Choose a Conda environment and start IPython",
                self.start_ipython,
                "utilities-terminal-symbolic",
            ),
            (
                "StartJupyterLab",
                "Start JupyterLab",
                "Choose a Conda environment and start JupyterLab",
                self.start_jupyterlab,
                "applications-science-symbolic",
            ),
            (
                "StartJupyterNotebook",
                "Start Jupyter Notebook",
                "Choose a Conda environment and start Jupyter Notebook",
                self.start_jupyter_notebook,
                "applications-science-symbolic",
            ),
        ]

        for name, label, tip, callback, icon in items:
            item = self.create_menu_item(
                name=f"DeveloperContextMenu::{name}",
                label=label,
                tip=tip,
                icon=icon,
            )
            item.connect("activate", callback, folder_path)
            submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # Git submenu
    # ================================================================

    def create_git_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the Git submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Git",
            label="Git",
            tip="Git repository tools",
            icon="git-symbolic",
        )

        submenu = Nautilus.Menu()

        items = [
            (
                "OpenGitTerminal",
                "Open Git Terminal Here",
                "Open a terminal at the repository root",
                self.open_git_terminal,
                "utilities-terminal-symbolic",
            ),
            (
                "GitStatus",
                "Git Status",
                "Show repository status",
                self.git_status,
                "dialog-information-symbolic",
            ),
            (
                "GitLog",
                "Git Log",
                "Show the latest commits",
                self.git_log,
                "view-list-symbolic",
            ),
            (
                "GitFetch",
                "Git Fetch",
                "Fetch changes from all remotes",
                self.git_fetch,
                "folder-download-symbolic",
            ),
            (
                "GitPull",
                "Git Pull",
                "Pull with fast-forward only",
                self.git_pull,
                "go-down-symbolic",
            ),
            (
                "GitPush",
                "Git Push",
                "Push the current branch",
                self.git_push,
                "go-up-symbolic",
            ),
            (
                "ShowGitBranch",
                "Show Current Branch",
                "Show branch and repository information",
                self.show_git_branch,
                "emblem-symbolic-link-symbolic",
            ),
            (
                "OpenGitRoot",
                "Open Repository Root",
                "Open the repository root in Files",
                self.open_git_root,
                "folder-open-symbolic",
            ),
            (
                "OpenGitRemote",
                "Open Remote Repository",
                "Open the origin repository in a browser",
                self.open_git_remote,
                "web-browser-symbolic",
            ),
        ]

        for name, label, tip, callback, icon in items:
            item = self.create_menu_item(
                name=f"DeveloperContextMenu::{name}",
                label=label,
                tip=tip,
                icon=icon,
            )
            item.connect("activate", callback, folder_path)
            submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # Docker submenu
    # ================================================================

    def create_docker_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the Docker submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Docker",
            label="Docker",
            tip="Docker and Docker Compose tools",
            icon="docker-symbolic",
        )

        submenu = Nautilus.Menu()

        if self.find_compose_file(folder_path):
            compose_items = [
                (
                    "ComposeUp",
                    "Compose Up",
                    "Start the Compose project in detached mode",
                    self.compose_up,
                    "media-playback-start-symbolic",
                ),
                (
                    "ComposeDown",
                    "Compose Down",
                    "Stop and remove the Compose project",
                    self.compose_down,
                    "media-playback-stop-symbolic",
                ),
                (
                    "ComposeRestart",
                    "Compose Restart",
                    "Restart services in the Compose project",
                    self.compose_restart,
                    "view-refresh-symbolic",
                ),
                (
                    "ComposeLogs",
                    "Compose Logs",
                    "Follow recent Compose service logs",
                    self.compose_logs,
                    "text-x-log-symbolic",
                ),
            ]

            for name, label, tip, callback, icon in compose_items:
                item = self.create_menu_item(
                    name=f"DeveloperContextMenu::{name}",
                    label=label,
                    tip=tip,
                    icon=icon,
                )
                item.connect("activate", callback, folder_path)
                submenu.append_item(item)

        global_items = [
            (
                "DockerContainers",
                "Docker Containers",
                "List running and stopped containers",
                self.docker_containers,
                "view-list-symbolic",
            ),
            (
                "DockerImages",
                "Docker Images",
                "List locally available images",
                self.docker_images,
                "drive-harddisk-symbolic",
            ),
            (
                "DockerDiskUsage",
                "Docker Disk Usage",
                "Show Docker disk-space usage",
                self.docker_disk_usage,
                "drive-harddisk-symbolic",
            ),
        ]

        for name, label, tip, callback, icon in global_items:
            item = self.create_menu_item(
                name=f"DeveloperContextMenu::{name}",
                label=label,
                tip=tip,
                icon=icon,
            )
            item.connect("activate", callback, folder_path)
            submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # AI Workstation submenu
    # ================================================================

    def create_ai_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the local AI-workstation submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::AIWorkstation",
            label="AI Workstation",
            tip="Local AI services, GPUs, CUDA and Ollama",
            icon="applications-science-symbolic",
        )

        submenu = Nautilus.Menu()

        items = [
            (
                "OpenDify",
                "Open Dify",
                "Open the locally hosted Dify interface",
                self.open_dify,
                "web-browser-symbolic",
            ),
            (
                "OpenOpenWebUI",
                "Open Open WebUI",
                "Open the locally hosted Open WebUI interface",
                self.open_openwebui,
                "web-browser-symbolic",
            ),
            (
                "OpenBentoPDF",
                "Open BentoPDF",
                "Open the locally hosted BentoPDF interface",
                self.open_bentopdf,
                "application-pdf-symbolic",
            ),
            (
                "OpenOllamaAPI",
                "Open Ollama API",
                "Open the Ollama model-list API endpoint",
                self.open_ollama_api,
                "network-server-symbolic",
            ),
            (
                "GPUStatus",
                "GPU Status",
                "Show NVIDIA GPU utilization and memory usage",
                self.show_gpu_status,
                "video-display-symbolic",
            ),
            (
                "CUDAInformation",
                "CUDA Information",
                "Show NVIDIA, CUDA toolkit and PyTorch CUDA information",
                self.show_cuda_information,
                "dialog-information-symbolic",
            ),
            (
                "OllamaStatus",
                "Ollama Service Status",
                "Check the Ollama executable, process and API",
                self.show_ollama_status,
                "network-server-symbolic",
            ),
            (
                "OllamaModels",
                "Installed Ollama Models",
                "List locally installed Ollama models",
                self.show_ollama_models,
                "view-list-symbolic",
            ),
            (
                "PullOllamaModel",
                "Pull Ollama Model",
                "Enter and download an Ollama model",
                self.pull_ollama_model,
                "folder-download-symbolic",
            ),
        ]

        for name, label, tip, callback, icon in items:
            item = self.create_menu_item(
                name=f"DeveloperContextMenu::{name}",
                label=label,
                tip=tip,
                icon=icon,
            )

            item.connect(
                "activate",
                callback,
                folder_path,
            )

            submenu.append_item(item)

        parent.set_submenu(submenu)

        return parent

    # ================================================================
    # Project submenu
    # ================================================================

    def create_project_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the context-sensitive Project submenu."""

        project = self.detect_project(folder_path)

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Project",
            label="Project",
            tip="Context-sensitive project tools",
            icon="folder-development-symbolic",
        )

        submenu = Nautilus.Menu()

        items = [
            (
                "ShowDetectedProject",
                "Show Detected Project",
                "Show detected project types and files",
                self.show_detected_project,
                "dialog-information-symbolic",
            ),
            (
                "OpenProjectTerminal",
                "Open Project Terminal",
                "Open a terminal at the detected project root",
                self.open_project_terminal,
                "utilities-terminal-symbolic",
            ),
        ]

        for name, label, tip, callback, icon in items:
            item = self.create_menu_item(
                name=f"DeveloperContextMenu::{name}",
                label=label,
                tip=tip,
                icon=icon,
            )
            item.connect("activate", callback, folder_path)
            submenu.append_item(item)

        if project.get("local_environment") or project.get("environment_file"):
            item = self.create_menu_item(
                name="DeveloperContextMenu::OpenDetectedEnvironment",
                label="Open Detected Environment",
                tip="Activate the detected Python environment",
                icon="utilities-terminal-symbolic",
            )
            item.connect(
                "activate",
                self.open_detected_environment,
                folder_path,
            )
            submenu.append_item(item)

        if project.get("python"):
            item = self.create_menu_item(
                name="DeveloperContextMenu::StartProjectJupyterLab",
                label="Start Project JupyterLab",
                tip="Start JupyterLab at the detected project root",
                icon="applications-science-symbolic",
            )
            item.connect(
                "activate",
                self.start_project_jupyterlab,
                folder_path,
            )
            submenu.append_item(item)

        if project.get("streamlit"):
            item = self.create_menu_item(
                name="DeveloperContextMenu::RunDetectedStreamlit",
                label="Run Streamlit",
                tip="Run the detected Streamlit application",
                icon="media-playback-start-symbolic",
            )
            item.connect(
                "activate",
                self.run_detected_streamlit,
                folder_path,
            )
            submenu.append_item(item)

        if project.get("fastapi"):
            item = self.create_menu_item(
                name="DeveloperContextMenu::RunDetectedFastAPI",
                label="Run FastAPI",
                tip="Run the detected FastAPI application",
                icon="media-playback-start-symbolic",
            )
            item.connect(
                "activate",
                self.run_detected_fastapi,
                folder_path,
            )
            submenu.append_item(item)

            docs_item = self.create_menu_item(
                name="DeveloperContextMenu::OpenFastAPIDocumentation",
                label="Open FastAPI Documentation",
                tip="Open http://localhost:8000/docs",
                icon="web-browser-symbolic",
            )
            docs_item.connect(
                "activate",
                self.open_fastapi_documentation,
                folder_path,
            )
            submenu.append_item(docs_item)

        if project.get("compose_file"):
            up_item = self.create_menu_item(
                name="DeveloperContextMenu::ProjectComposeUp",
                label="Project Compose Up",
                tip="Start Compose from the detected project root",
                icon="media-playback-start-symbolic",
            )
            up_item.connect(
                "activate",
                self.project_compose_up,
                folder_path,
            )
            submenu.append_item(up_item)

            down_item = self.create_menu_item(
                name="DeveloperContextMenu::ProjectComposeDown",
                label="Project Compose Down",
                tip="Stop Compose from the detected project root",
                icon="media-playback-stop-symbolic",
            )
            down_item.connect(
                "activate",
                self.project_compose_down,
                folder_path,
            )
            submenu.append_item(down_item)

        if project.get("modelfile"):
            item = self.create_menu_item(
                name="DeveloperContextMenu::BuildDetectedOllamaModel",
                label="Build Ollama Model",
                tip="Build from the detected Modelfile",
                icon="system-run-symbolic",
            )
            item.connect(
                "activate",
                self.build_detected_ollama_model,
                folder_path,
            )
            submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # New Project submenu
    # ================================================================

    def create_new_project_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the New Project submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::NewProject",
            label="New Project",
            tip="Create a structured development project",
            icon="folder-new-symbolic",
        )

        submenu = Nautilus.Menu()

        item = self.create_menu_item(
            name="DeveloperContextMenu::NewProjectWizard",
            label="Create New Project…",
            tip="Open New Project Wizard v3.1",
            icon="document-new-symbolic",
        )

        item.connect(
            "activate",
            self.new_project_wizard,
            folder_path,
        )

        submenu.append_item(item)
        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # Utilities submenu
    # ================================================================

    def create_utilities_menu(
        self,
        folder_path: str,
    ) -> Nautilus.MenuItem:
        """Build the Utilities submenu."""

        parent = self.create_menu_item(
            name="DeveloperContextMenu::Utilities",
            label="Utilities",
            tip="General developer utilities",
            icon="applications-utilities-symbolic",
        )

        submenu = Nautilus.Menu()

        item = self.create_menu_item(
            name="DeveloperContextMenu::OpenTerminal",
            label="Open Terminal Here",
            tip="Open GNOME Terminal in this folder",
            icon="utilities-terminal-symbolic",
        )

        item.connect("activate", self.open_terminal, folder_path)
        submenu.append_item(item)

        parent.set_submenu(submenu)
        return parent

    # ================================================================
    # Main Developer menu
    # ================================================================

    def create_developer_menu(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> list[Nautilus.MenuItem]:
        """Build the complete structured Developer menu."""

        folder_path = self.get_local_path(current_folder)

        if not folder_path:
            return []

        folder_path = str(Path(folder_path).expanduser().resolve())

        developer_parent = self.create_menu_item(
            name="DeveloperContextMenu::Developer",
            label="Developer",
            tip="Developer and AI-workstation tools",
            icon="applications-development-symbolic",
        )

        developer_submenu = Nautilus.Menu()

        developer_submenu.append_item(self.create_editors_menu(folder_path))

        if self.find_conda_executable():
            developer_submenu.append_item(self.create_python_menu(folder_path))

        if self.find_command(["git"]):
            developer_submenu.append_item(self.create_git_menu(folder_path))

        if self.find_command(["docker"]):
            developer_submenu.append_item(self.create_docker_menu(folder_path))

        developer_submenu.append_item(self.create_ai_menu(folder_path))

        developer_submenu.append_item(self.create_project_menu(folder_path))

        developer_submenu.append_item(self.create_new_project_menu(folder_path))

        developer_submenu.append_item(self.create_utilities_menu(folder_path))

        developer_parent.set_submenu(developer_submenu)

        return [developer_parent]

    # ================================================================
    # Nautilus MenuProvider interface
    # ================================================================

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> list[Nautilus.MenuItem]:
        """Show the menu when right-clicking empty folder space."""

        return self.create_developer_menu(current_folder)

    def get_file_items(
        self,
        files: list[Nautilus.FileInfo],
    ) -> list[Nautilus.MenuItem]:
        """Show the menu when right-clicking one local folder."""

        if len(files) != 1:
            return []

        selected_item = files[0]

        if not selected_item.is_directory():
            return []

        return self.create_developer_menu(selected_item)
