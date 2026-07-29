"""Project-detection utility functions."""

from collections.abc import Mapping
from pathlib import Path

from .docker_utils import find_compose_file
from .filesystem import file_contains_any, find_python_files, search_upwards
from .git_utils import get_git_root


def detect_project_root(folder_path: str) -> str:
    """Return the most likely project root."""

    git_root = get_git_root(folder_path)

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


def detect_project(folder_path: str) -> dict[str, str | bool | None]:
    """Inspect the selected folder and identify project capabilities."""

    root = Path(detect_project_root(folder_path)).expanduser().resolve()

    project: dict[str, str | bool | None] = {
        "root": str(root),
        "git": get_git_root(str(root)) is not None,
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

    compose_file = find_compose_file(str(root))

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

    ordered_fastapi_files.extend(path for path in python_files if path not in ordered_fastapi_files)

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


def project_report(project: Mapping[str, object]) -> str:
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
