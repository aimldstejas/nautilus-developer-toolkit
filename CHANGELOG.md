# Changelog

All notable changes to **Nautilus Developer Toolkit (NDT)** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

Development under this section represents work completed after the stable `v1.0.0` baseline.

The current work is part of the incremental Version 2 modular-refactoring effort and has not yet been released as a stable Version 2 version.

### Added

#### Repository and Development Workflow

- Established the public GitHub repository and the stable `main` branch.
- Established the `develop` integration branch and focused Version 2 feature branches.
- Added repository-quality checks, local linting, type checking, testing, and GitHub Actions workflows.

#### Modular Package Foundation

- Added the Python package root:

```text
src/nautilus_developer_toolkit/
```

- Established initial service, integration, and utility package namespaces for incremental Version 2 development.
- Preserved the principle that optional AI services and external integrations remain separate from the core toolkit.

#### Utility Extraction

- Added focused reusable utilities under:

```text
src/nautilus_developer_toolkit/utils/
```

- Extracted reusable command, filesystem, path, notification, Conda, process, Git, Docker Compose, menu-item, project-root, project-detection, and project-report responsibilities from `developer_context_menu.py`.
- Updated the active Version 2 development source to use extracted utilities through compatibility wrappers where verified.

#### Testing and Quality

- Added the pytest test structure and focused unit tests for extracted utility responsibilities.
- Added Ruff, mypy, pre-commit, and repository workflow checks.

### Changed

#### Architecture

- Began the Version 2 migration from a single-file architecture to a modular package architecture.
- Adopted incremental extraction instead of a wholesale rewrite.
- Preserved the frozen Version 1 snapshot as the authoritative stable baseline.
- Retained `DeveloperContextMenu` as the Nautilus integration, UI presentation, workflow coordination, notification, process, and menu-construction boundary.

#### Completed Utility-Extraction Phase

- **Version 2 utility-extraction phase complete.**
- Reusable non-UI logic now resides in focused modules under `src/nautilus_developer_toolkit/utils/`.
- Compatibility wrappers remain in `DeveloperContextMenu` to preserve verified existing call sites and class-level behavior.
- Focused unit-test coverage was expanded, with a final validated baseline of `96` passing unit tests.
- This phase introduced no intended user-facing behavior change and continues the separation of reusable logic from Nautilus UI orchestration.

#### Documentation

- Completed documentation synchronization for the utility-extraction milestone.
- Recorded the implemented utility-layer architecture, completed utility-extraction status, and remaining Version 2 work.
- The next step is integration review and merge preparation.

### Fixed

#### Refactoring and Code Quality

- Resolved lint, type, import, and module-boundary issues encountered during controlled modularization.
- Preserved extracted behavior through focused tests and compatibility wrappers.

### Security

- No known security vulnerabilities were introduced by the current Version 2 development work.
- No credentials, API keys, model files, raw datasets, or private configuration files are intentionally tracked.
- Optional AI and local-service integrations remain separated from the core toolkit.
- The protected `main` branch remains the stable release boundary.

### Development Notes

- Version 2 remains under active development and is not yet a stable release.
- `developer_context_menu.py` remains partially responsible for application behavior through orchestration and UI-bound methods.
- Further extraction is not automatically beneficial where it would fragment coordinated workflows.
- Integration review and merge preparation are the next controlled steps.

---

## [1.0.0] - 2026-07-28

Version `1.0.0` is the stable and frozen baseline of the original Nautilus Developer Toolkit implementation.

### Added

#### Developer Experience

- Native Nautilus developer context menu.
- Integrated editor launchers.
- Integrated terminal launcher.
- Context-aware actions for folders and detected projects.

#### Editor Integration

- gedit launcher.
- VSCodium launcher.
- PyCharm launcher.

#### Terminal Integration

- Open Terminal Here action.

#### Python Support

- Automatic Python project detection.
- Virtual-environment detection and support.
- Conda-environment detection and support.
- Environment-activation support.
- IPython launcher.
- Jupyter Notebook launcher.
- JupyterLab launcher.
- Streamlit application support.
- FastAPI application support.

#### Git Integration

- Git repository detection.
- Repository status.
- Current branch information.
- Remote repository information.
- Fetch operation.
- Pull operation.
- Push operation.
- Git log viewer.

#### Docker Integration

- Docker project detection.
- Docker Compose Up.
- Docker Compose Down.
- Docker Compose Restart.
- Container-management utilities.
- Image-management utilities.
- Docker disk-usage information.
- Docker log viewer.

#### Local AI Integration

- Ollama launcher.
- Ollama model listing.
- Ollama model-build support.
- Dify launcher.
- Open WebUI launcher.
- BentoPDF launcher.

#### GPU and CUDA Utilities

- NVIDIA GPU information.
- CUDA information.

#### Smart Project Detection

Automatic detection of:

- Git repositories
- Python projects
- Virtual environments
- Conda environments
- Docker projects
- Streamlit applications
- FastAPI applications
- Jupyter projects
- Ollama Modelfiles

#### Project Actions

- Project-identification utilities.
- Environment activation.
- Streamlit execution.
- FastAPI execution.
- FastAPI documentation launcher.
- Docker Compose controls.
- Ollama model-build support.

#### Project Wizard

- Automated project creation.
- Multiple project templates.
- Automated virtual-environment setup.
- Dependency installation.
- Editor launch.
- Sequential project setup.
- Automatic application startup where applicable.

Project templates include:

- Basic Python
- Data Science
- Streamlit
- FastAPI
- Docker
- Retrieval-Augmented Generation
- AI Agent
- Model Context Protocol server

#### Documentation and Community Infrastructure

- Added the initial public repository structure.
- Added the MIT license.
- Added the project README.
- Added installation documentation.
- Added quick-start documentation.
- Added a user guide.
- Added configuration documentation.
- Added Project Wizard documentation.
- Added Git documentation.
- Added Docker documentation.
- Added Python documentation.
- Added AI-integration documentation.
- Added troubleshooting documentation.
- Added frequently asked questions.
- Added changelog-maintenance guidance.
- Added development guidelines.
- Added contribution guidelines.
- Added a code of conduct.
- Added security-reporting guidance.
- Added support guidance.
- Added the project roadmap.
- Added the architecture document.
- Added GitHub issue templates.
- Added a pull-request template.
- Added project metadata and dependency files.

#### Version Preservation

- Added a frozen snapshot of the working Version 1 extension.
- Verified the frozen snapshot against the working extension using SHA256.
- Created the stable `v1.0.0` Git tag.

### Changed

- Established the initial professional repository structure.
- Defined the project’s engineering and contribution standards.
- Defined the long-term Version 2 and Version 3 architectural direction.
- Improved the Project Wizard workflow to use sequential setup and application launch.
- Standardized the permanent project name as Nautilus Developer Toolkit.
- Standardized the project abbreviation as NDT.

### Fixed

- Improved Project Wizard stability.
- Improved sequential environment setup.
- Improved dependency-installation behavior.
- Improved editor-launch behavior.
- Improved automatic application startup.
- Applied stability and usability corrections before the initial stable release.

### Security

- Added a security policy and vulnerability-reporting process.
- Reviewed the initial repository for obvious credential and secret exposure.
- No known security vulnerabilities were identified at the time of release.

---

## Known Version 1 Limitations

Version `1.0.0` has the following known architectural limitations:

- Monolithic single-file implementation.
- No user-facing configuration system.
- No plugin architecture.
- Limited automated test coverage.
- No GitHub Actions CI/CD workflow.
- No Linux distribution packaging.
- Some integrations depend on locally installed applications or services.
- GNOME and Nautilus APIs provide incomplete static type information.
- Optional integrations may not be available on every system.

These limitations are the primary focus of the Version 2 development line.

---

## Version 1.0.0 Notes

Version `1.0.0` represents the stable baseline of the original working implementation.

The release is intentionally frozen so that Version 2 can be developed through controlled modular extraction without losing a known-good reference implementation.

Future development focuses on:

- Modular architecture
- Improved test coverage
- Separation of menu and operational logic
- Configuration management
- Plugin architecture
- Packaging and distribution
- Local CI/CD
- Long-term maintainability
- Backward compatibility wherever practical

The frozen Version 1 snapshot must remain unchanged.

---

[Unreleased]: https://github.com/aimldstejas/nautilus-developer-toolkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/aimldstejas/nautilus-developer-toolkit/releases/tag/v1.0.0
