# Changelog

All notable changes to **Nautilus Developer Toolkit (NDT)** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

Development under this section represents work completed after the stable `v1.0.0` baseline.

The current work is part of the incremental Version 2 modular-refactoring effort and has not yet been released as a stable Version 2 version.

### Added

#### Repository and Development Workflow

* Created the public GitHub repository:
  `aimldstejas/nautilus-developer-toolkit`.
* Established `main` as the protected stable branch.
* Created the `develop` integration branch.
* Created focused Version 2 feature branches, including:

  * `feature/v2-modular-architecture`
  * `feature/v2-utils-extraction`
* Added pre-commit repository-quality checks.
* Added local linting, type-checking, and testing workflows.

#### Modular Package Foundation

* Added the Python package root:

  ```text
  src/nautilus_developer_toolkit/
  ```

* Added an initial service layer for separating operational logic from Nautilus menu presentation.

* Added service modules for:

  * AI-related operations
  * Conda environments
  * CUDA information
  * Docker operations
  * Git operations
  * Project operations
  * Streamlit applications
  * Terminal launching
  * VSCodium launching

* Added shared service exceptions.

#### Optional Integration Layer

* Added dedicated integration modules for:

  * BentoPDF
  * Dify
  * Ollama
  * Open WebUI
* Preserved the project principle that AI services and external integrations remain optional.

#### Utility Extraction

* Added a dedicated utility package under:

  ```text
  src/nautilus_developer_toolkit/utils/
  ```

* Extracted low-dependency filesystem helpers from the monolithic extension.

* Extracted low-dependency path helpers from the monolithic extension.

* Updated the active Version 2 development source to use the extracted utility modules while preserving existing behavior.

#### Testing

* Added a pytest test structure.
* Added unit tests for filesystem utilities.
* Added unit tests for path utilities.
* Established an initial passing test suite of 10 tests.
* Added tests alongside the first controlled utility-extraction milestone.

#### Code Quality

* Added Ruff configuration and lint checks.
* Added Mypy configuration and static type checking.
* Added pre-commit checks for:

  * Large files
  * Case conflicts
  * Merge conflicts
  * TOML files
  * YAML files
  * End-of-file consistency
  * Mixed line endings
  * Trailing whitespace

### Changed

#### Architecture

* Began the Version 2 migration from a single-file architecture to a modular package architecture.
* Adopted incremental extraction instead of a wholesale rewrite.
* Separated initial operational responsibilities into service modules.
* Separated optional local-service integrations into dedicated integration modules.
* Moved reusable filesystem and path behavior out of `developer_context_menu.py`.
* Established a lower-dependency-first extraction strategy.
* Preserved the frozen Version 1 snapshot as the authoritative stable baseline.

#### Development Process

* Replaced direct development on the stable branch with a feature-branch workflow.
* Introduced focused, reviewable commits for architectural extractions.
* Required extracted behavior to be accompanied by tests where practical.
* Established the local validation sequence of linting, type checking, testing, and pre-commit checks.
* Deferred GitHub Actions and CI workflow creation until the local modular architecture and test foundation are more mature.

#### Documentation

* Updated `PROJECT_CONTEXT.md` to reflect:

  * Git initialization
  * Public GitHub publication
  * Branch structure
  * Branch protection
  * Version `1.0.0` tagging
  * Version 2 development
  * Modular package progress
  * Utility extraction
  * Current testing and quality-tool status
* Updated the changelog to record completed post-`v1.0.0` development.

### Fixed

#### Refactoring and Code Quality

* Resolved Ruff lint issues encountered during the initial modularization work.
* Resolved initial Mypy issues across the checked modular source.
* Corrected import and module-boundary issues introduced during early extraction work.
* Preserved existing filesystem and path behavior after moving helpers into utility modules.
* Verified that the current pytest suite passes after the utility extraction.
* Verified that configured pre-commit checks pass for the committed extraction work.

### Security

* No known security vulnerabilities were introduced by the current Version 2 development work.
* No credentials, API keys, model files, raw datasets, or private configuration files are intentionally tracked.
* Optional AI and local-service integrations remain separated from the core toolkit.
* The protected `main` branch remains the stable release boundary.

### Development Notes

* Version 2 remains under active development and is not yet a stable release.
* The monolithic `developer_context_menu.py` remains partially responsible for application behavior.
* A dedicated formatting-only pass has not yet been performed on the monolithic source.
* `ruff format --check` may continue to report that the monolithic source would be reformatted.
* Formatting-only changes should not be mixed with functional extraction commits.
* GitHub Actions and other CI workflows remain intentionally deferred.
* The next refactoring steps should continue with the lowest-dependency helpers before extracting high-coupling Nautilus menu logic.

---

## [1.0.0] - 2026-07-28

Version `1.0.0` is the stable and frozen baseline of the original Nautilus Developer Toolkit implementation.

### Added

#### Developer Experience

* Native Nautilus developer context menu.
* Integrated editor launchers.
* Integrated terminal launcher.
* Context-aware actions for folders and detected projects.

#### Editor Integration

* gedit launcher.
* VSCodium launcher.
* PyCharm launcher.

#### Terminal Integration

* Open Terminal Here action.

#### Python Support

* Automatic Python project detection.
* Virtual-environment detection and support.
* Conda-environment detection and support.
* Environment-activation support.
* IPython launcher.
* Jupyter Notebook launcher.
* JupyterLab launcher.
* Streamlit application support.
* FastAPI application support.

#### Git Integration

* Git repository detection.
* Repository status.
* Current branch information.
* Remote repository information.
* Fetch operation.
* Pull operation.
* Push operation.
* Git log viewer.

#### Docker Integration

* Docker project detection.
* Docker Compose Up.
* Docker Compose Down.
* Docker Compose Restart.
* Container-management utilities.
* Image-management utilities.
* Docker disk-usage information.
* Docker log viewer.

#### Local AI Integration

* Ollama launcher.
* Ollama model listing.
* Ollama model-build support.
* Dify launcher.
* Open WebUI launcher.
* BentoPDF launcher.

#### GPU and CUDA Utilities

* NVIDIA GPU information.
* CUDA information.

#### Smart Project Detection

Automatic detection of:

* Git repositories
* Python projects
* Virtual environments
* Conda environments
* Docker projects
* Streamlit applications
* FastAPI applications
* Jupyter projects
* Ollama Modelfiles

#### Project Actions

* Project-identification utilities.
* Environment activation.
* Streamlit execution.
* FastAPI execution.
* FastAPI documentation launcher.
* Docker Compose controls.
* Ollama model-build support.

#### Project Wizard

* Automated project creation.
* Multiple project templates.
* Automated virtual-environment setup.
* Dependency installation.
* Editor launch.
* Sequential project setup.
* Automatic application startup where applicable.

Project templates include:

* Basic Python
* Data Science
* Streamlit
* FastAPI
* Docker
* Retrieval-Augmented Generation
* AI Agent
* Model Context Protocol server

#### Documentation and Community Infrastructure

* Added the initial public repository structure.
* Added the MIT license.
* Added the project README.
* Added installation documentation.
* Added quick-start documentation.
* Added a user guide.
* Added configuration documentation.
* Added Project Wizard documentation.
* Added Git documentation.
* Added Docker documentation.
* Added Python documentation.
* Added AI-integration documentation.
* Added troubleshooting documentation.
* Added frequently asked questions.
* Added changelog-maintenance guidance.
* Added development guidelines.
* Added contribution guidelines.
* Added a code of conduct.
* Added security-reporting guidance.
* Added support guidance.
* Added the project roadmap.
* Added the architecture document.
* Added GitHub issue templates.
* Added a pull-request template.
* Added project metadata and dependency files.

#### Version Preservation

* Added a frozen snapshot of the working Version 1 extension.
* Verified the frozen snapshot against the working extension using SHA256.
* Created the stable `v1.0.0` Git tag.

### Changed

* Established the initial professional repository structure.
* Defined the project’s engineering and contribution standards.
* Defined the long-term Version 2 and Version 3 architectural direction.
* Improved the Project Wizard workflow to use sequential setup and application launch.
* Standardized the permanent project name as Nautilus Developer Toolkit.
* Standardized the project abbreviation as NDT.

### Fixed

* Improved Project Wizard stability.
* Improved sequential environment setup.
* Improved dependency-installation behavior.
* Improved editor-launch behavior.
* Improved automatic application startup.
* Applied stability and usability corrections before the initial stable release.

### Security

* Added a security policy and vulnerability-reporting process.
* Reviewed the initial repository for obvious credential and secret exposure.
* No known security vulnerabilities were identified at the time of release.

---

## Known Version 1 Limitations

Version `1.0.0` has the following known architectural limitations:

* Monolithic single-file implementation.
* No user-facing configuration system.
* No plugin architecture.
* Limited automated test coverage.
* No GitHub Actions CI/CD workflow.
* No Linux distribution packaging.
* Some integrations depend on locally installed applications or services.
* GNOME and Nautilus APIs provide incomplete static type information.
* Optional integrations may not be available on every system.

These limitations are the primary focus of the Version 2 development line.

---

## Version 1.0.0 Notes

Version `1.0.0` represents the stable baseline of the original working implementation.

The release is intentionally frozen so that Version 2 can be developed through controlled modular extraction without losing a known-good reference implementation.

Future development focuses on:

* Modular architecture
* Improved test coverage
* Separation of menu and operational logic
* Configuration management
* Plugin architecture
* Packaging and distribution
* Local CI/CD
* Long-term maintainability
* Backward compatibility wherever practical

The frozen Version 1 snapshot must remain unchanged.

---

[Unreleased]: https://github.com/aimldstejas/nautilus-developer-toolkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/aimldstejas/nautilus-developer-toolkit/releases/tag/v1.0.0
