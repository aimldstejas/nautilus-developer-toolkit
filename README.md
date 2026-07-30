# Nautilus Developer Toolkit (NDT)

> Transform the Linux file manager into a developer workspace.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Desktop](https://img.shields.io/badge/desktop-GNOME%20%7C%20Nautilus-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**Nautilus Developer Toolkit (NDT)** is an open-source Nautilus extension that brings software-development tools, project actions, container workflows, and optional local AI integrations directly into the Linux file manager.

Instead of repeatedly opening terminals, changing directories, activating environments, and remembering commands, developers can right-click inside a project folder and launch context-aware actions from Nautilus.

NDT is designed around four principles:

- Linux-first
- Local-first
- Transparent automation
- Optional AI integration

---

## Table of Contents

- [Why NDT?](#why-ndt)
- [Key Features](#key-features)
- [Project Wizard](#project-wizard)
- [Supported Tools](#supported-tools)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Documentation](#documentation)
- [Project Architecture](#project-architecture)
- [Development Status](#development-status)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)
- [License](#license)

---

## Why NDT?

Many development tasks begin with the same repetitive sequence:

1. Open a terminal.
2. Navigate to the project directory.
3. Activate an environment.
4. Enter a command.
5. Wait for a service to start.
6. Open an editor or browser.

NDT reduces this repetition by exposing development actions directly inside Nautilus.

A project folder can provide relevant actions for:

- Editors
- Terminals
- Python environments
- Git repositories
- Docker projects
- Streamlit applications
- FastAPI applications
- Jupyter projects
- Local AI services
- NVIDIA GPUs and CUDA
- Project generation

The available context-menu actions adapt to the selected directory and detected project type.

---

# Key Features

## Smart Project Detection

NDT automatically detects common development projects and environments, including:

- Git repositories
- Python projects
- Python virtual environments
- Conda environments
- Docker projects
- Streamlit applications
- FastAPI applications
- Jupyter projects
- Ollama Modelfiles

Detected project information is used to display relevant context-menu actions.

---

## Editor and Terminal Integration

Open supported development tools directly in the selected directory.

Current integrations include:

- gedit
- VSCodium
- PyCharm
- GNOME Terminal

Typical actions include:

- Open gedit Here
- Open VSCodium Here
- Open PyCharm Here
- Open Terminal Here
- Open environment-aware terminal

---

## Python Development

NDT provides shortcuts for common Python development workflows.

Current capabilities include:

- Python project detection
- Virtual-environment detection
- Conda-environment detection
- Environment-aware terminals
- IPython
- Jupyter Notebook
- JupyterLab
- Streamlit execution
- FastAPI execution
- FastAPI documentation launcher

---

## Git Integration

Common Git information and operations are available directly from Nautilus.

Current actions include:

- Show repository status
- Show current branch
- Show repository root
- Show remote repository information
- View Git log
- Fetch
- Pull
- Push

Git actions appear only when an applicable repository is detected.

---

## Docker Integration

NDT provides project-aware Docker and Docker Compose actions.

Current capabilities include:

- Docker project detection
- Docker Compose Up
- Docker Compose Down
- Docker Compose Restart
- View logs
- List containers
- List images
- Show Docker disk usage

---

## Local AI Integration

NDT can integrate with locally hosted AI and document-processing services.

Current integrations include:

- Ollama
- Dify
- Open WebUI
- BentoPDF

Additional utilities include:

- List installed Ollama models
- Build an Ollama model from a Modelfile
- Show NVIDIA GPU information
- Show CUDA information

These integrations are optional.

The core toolkit does not require an AI service, cloud account, or remote API.

---

## Project Actions

Project-specific actions become available automatically when supported files or environments are detected.

Examples include:

- Show detected project
- Open project terminal
- Activate project environment
- Run Streamlit application
- Run FastAPI application
- Open FastAPI documentation
- Start Docker Compose services
- Stop Docker Compose services
- Build Ollama model

---

# Project Wizard

The integrated Project Wizard generates starter projects and can perform common setup tasks.

## Current Templates

- Basic Python
- Data Science
- Streamlit
- FastAPI
- Docker Compose
- Retrieval-Augmented Generation application
- AI Agent application
- Model Context Protocol server

## Optional Setup Actions

Depending on the selected template, the wizard can:

- Create the project directory
- Generate starter files
- Initialize Git
- Create a Python virtual environment
- Create a Conda environment
- Install dependencies
- Open the project in VSCodium
- Launch the generated application
- Open a browser after the application is ready

Generated projects are intended to remain understandable and editable rather than hiding their structure behind opaque automation.

---

# Supported Tools

NDT can interact with the following tools when they are installed or available on the system.

| Category         | Tools and services                           |
| ---------------- | -------------------------------------------- |
| File manager     | Nautilus                                     |
| Editors          | gedit, VSCodium, PyCharm                     |
| Terminal         | GNOME Terminal                               |
| Python           | Python, virtual environments, Conda, IPython |
| Notebooks        | Jupyter Notebook, JupyterLab                 |
| Web applications | Streamlit, FastAPI                           |
| Version control  | Git                                          |
| Containers       | Docker, Docker Compose                       |
| Local AI         | Ollama, Dify, Open WebUI                     |
| Documents        | BentoPDF                                     |
| GPU utilities    | NVIDIA tools, CUDA                           |

NDT does not install all of these applications automatically. Menu actions depend on the corresponding tools being available on the host system.

---

# Installation

NDT is currently distributed from source.

The current stable public release is Version `1.0.0` at tag `v1.0.0`. The `develop` branch contains unreleased Version 2 development at `2.0.0.dev0`; it uses a modular package plus the repository-root Nautilus extension entrypoint and is not yet stable.

See the complete installation instructions:

- [Installation Guide](docs/INSTALLATION.md)
- [Quick Start](docs/QUICK_START.md)
- [Version 1 to Version 2 Development Migration Guide](docs/MIGRATION_GUIDE.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

A typical source installation requires:

- Linux with GNOME and Nautilus
- Python 3.11 or later
- `nautilus-python`
- PyGObject and the applicable GNOME bindings

After installing or updating a Nautilus Python extension, Nautilus may need to be restarted before the new context-menu items appear.

---

# Compatibility

## Primary Development Platform

NDT is currently developed and tested primarily on:

- Ubuntu 24.04 LTS
- GNOME
- Nautilus
- Python 3.11+
- `nautilus-python`

## Additional Linux Distributions

Compatibility with additional GNOME-based Linux distributions is planned.

Behavior may vary depending on:

- Distribution packaging
- Nautilus version
- GNOME version
- Python version
- Terminal application
- Installed editors
- Docker installation
- Conda installation
- Availability of optional local services

Compatibility reports and contributions are welcome.

---

# Documentation

Project documentation is maintained in the [`docs/`](docs/) directory.

Available documentation includes:

- [Installation](docs/INSTALLATION.md)
- [Quick Start](docs/QUICK_START.md)
- [Migration Guide](docs/MIGRATION_GUIDE.md)
- [User Guide](docs/USER_GUIDE.md)
- [Configuration](docs/CONFIGURATION.md)
- [Project Wizard](docs/PROJECT_WIZARD.md)
- [Python Integration](docs/PYTHON.md)
- [Git Integration](docs/GIT.md)
- [Docker Integration](docs/DOCKER.md)
- [AI Integration](docs/AI_INTEGRATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Frequently Asked Questions](docs/FAQ.md)
- [Changelog Guide](docs/CHANGELOG_GUIDE.md)

Additional project-level documents include:

- [Architecture](ARCHITECTURE.md)
- [Development Guidelines](DEVELOPMENT_GUIDELINES.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Security Policy](SECURITY.md)
- [Support Guide](SUPPORT.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Current Project Context](PROJECT_CONTEXT.md)

---

# Project Architecture

## Version 1

Version 1 uses a stable single-file Nautilus extension.

The Version 1 implementation is frozen and preserved as the known-working baseline.

A verified snapshot is stored under:

```text
snapshots/
```

The frozen snapshot must not be modified during Version 2 development.

## Version 2

Version 2 is being developed through incremental modular extraction rather than a wholesale rewrite.

The current package foundation is located under:

```text
src/nautilus_developer_toolkit/
```

Current modular areas include:

```text
src/nautilus_developer_toolkit/
├── integrations/
├── services/
└── utils/
```

The architecture is expected to evolve toward:

```text
src/nautilus_developer_toolkit/
├── extension.py
├── menus/
├── detectors/
├── integrations/
├── plugins/
├── services/
├── templates/
└── utils/
```

Directories and modules are introduced only when they represent a real responsibility.

The refactoring strategy is to:

1. Extract low-dependency helpers first.
2. Preserve existing behavior.
3. Add focused unit tests.
4. Keep commits small and reviewable.
5. Separate Nautilus presentation logic from operational logic.
6. Avoid premature abstraction.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the architectural direction.

---

# Development Status

## Stable Release

**Current stable version:** `1.0.0`

**Stable tag:** `v1.0.0`

Version 1.0 is:

- Stable
- Frozen
- Documented
- Published
- Preserved through a verified source snapshot

## Version 2 Development

**Current development version:** `2.0.0.dev0` on `develop`

Version 2 is not yet a stable release.

Completed foundations include:

- Modular Python package structure
- Service-layer and optional integration namespaces
- Focused reusable utility modules
- Compatibility wrappers in `DeveloperContextMenu` where verified
- Focused unit-test coverage for extracted utility responsibilities
- Ruff linting, mypy type checking, pre-commit checks, and repository workflows
- Integration of the modular architecture and extracted utilities into `develop`
- Version and packaging metadata alignment
- Warning-free isolated wheel and source-distribution validation

Reusable non-UI logic now resides in focused utility modules, while `DeveloperContextMenu` remains the Nautilus integration, UI presentation, workflow coordination, notification, process, and menu-construction boundary.

The utility-extraction phase introduced no intended user-facing behavior change. The Version 2 implementation is not yet a stable release, and this milestone does not mark all Version 2 work as complete.

Current release-readiness work covers documentation, external GitHub metadata, clean system-Python installation and Nautilus deployment validation, and a future release-candidate phase before any stable Version 2 release.

## Branch Model

The repository uses:

- `main` for stable, reviewed history
- `develop` for integration
- Focused feature branches for Version 2 development

The default branch, `main`, is protected by the active repository ruleset `Protect main` (ID `19731984`). Changes require a pull request, successful `quality`, `tests (3.11)`, and `tests (3.12)` checks, resolved review conversations, and an up-to-date branch. Force-pushes and branch deletion are blocked.

---

# Quality Standards

The project follows these engineering standards:

- Python 3.11+
- PEP 8
- Semantic Versioning
- Type hints where practical
- Single Responsibility Principle
- Composition preferred over inheritance
- Readability over cleverness
- Backward compatibility wherever practical
- Tests for extracted behavior
- Small, focused commits
- Local-first operation
- Optional AI and cloud integrations

Current development checks include:

```text
ruff check
mypy
pytest
pre-commit
```

Local quality checks and GitHub Actions workflows support the current Version 2 development branch. Release-readiness validation must finish before release-candidate preparation or a controlled pull request to `main`.

---

# Roadmap

## Version 1.x — Stabilization

Focus areas:

- Stable baseline maintenance
- Bug fixes
- Documentation improvements
- Compatibility testing
- Installation improvements
- Packaging preparation
- Regression tests

## Version 2.0 — Modular Architecture

Goals include:

- Modular package structure
- Separation of menu and operational logic
- Dedicated detector modules
- Dedicated services
- Reusable utilities
- Configuration system
- Expanded automated testing
- Improved maintainability
- Backward-compatible migration

## Version 2.5 — Plugin Architecture

Planned capabilities include:

- Plugin discovery
- Plugin registration
- Contributor-facing plugin interfaces
- Git plugin
- Docker plugin
- AWS plugin
- Ollama plugin
- Dify plugin

## Version 3.x — AI-Assisted Development

Planned capabilities include:

- AI Project Generator
- Repository Chat
- Repository Explanation
- AI Code Review
- Test generation
- Documentation generation
- Log analysis
- Traceback analysis
- Assisted refactoring
- Plugin SDK

AI capabilities will remain optional and will not be required for the core toolkit.

See [ROADMAP.md](ROADMAP.md) for the detailed roadmap.

---

# Contributing

Contributions are welcome.

Useful contribution areas include:

- Bug fixes
- Automated tests
- Documentation
- Linux-distribution compatibility
- Project templates
- Editor integrations
- Developer-tool integrations
- Accessibility improvements
- Packaging
- Future plugin development

Before contributing, read:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [DEVELOPMENT_GUIDELINES.md](DEVELOPMENT_GUIDELINES.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

Please use focused branches and keep changes limited to one coherent responsibility wherever practical.

---

# Security

Do not report security vulnerabilities through a public issue.

Follow the process described in:

- [SECURITY.md](SECURITY.md)

Do not commit:

- Passwords
- API keys
- Access tokens
- Private keys
- Personal configuration files
- Local service credentials
- Environment files containing secrets

---

# Support

For installation help, known limitations, and troubleshooting guidance, see:

- [SUPPORT.md](SUPPORT.md)
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- [FAQ.md](docs/FAQ.md)

When reporting a problem, include:

- Linux distribution and version
- GNOME version
- Nautilus version
- Python version
- Installation method
- Relevant logs or error messages
- Steps needed to reproduce the issue

Remove credentials and other sensitive information before sharing logs.

---

# License

Nautilus Developer Toolkit is released under the [MIT License](LICENSE).

---

# Project Status Summary

| Area | Status |
| --- | --- |
| Version 1.0 implementation | Stable and frozen |
| Public GitHub repository | Available |
| Documentation foundation | Complete |
| Utility-extraction milestone documentation | Complete |
| Version 1.0 tag | Created |
| Stable Version 1 boundary | `main` at tag `v1.0.0` |
| GitHub branch protection | Active repository ruleset `Protect main` (ID `19731984`) |
| Version 2 modularization | Integrated into `develop` |
| Utility-extraction phase | Complete |
| Version 2 development version | `2.0.0.dev0` (unreleased) |
| Unit testing | `96` unit tests passing |
| Local quality checks and GitHub Actions | Passing |
| Release and migration documentation | Current |
| Clean system-Python and Nautilus deployment validation | Pending |
| Release-candidate preparation | Future controlled phase |
| Plugin architecture | Planned |
| Configuration system | Planned |
| Python package build | Wheel and source distribution validated |
| AI-assisted development | Planned for Version 3 |

---

NDT aims to make the Linux file manager a practical entry point for everyday software-development workflows while keeping automation visible, understandable, and under the developer’s control.
