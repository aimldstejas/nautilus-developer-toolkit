# Nautilus Developer Toolkit (NDT)

> Living project context document.
>
> This file records the authoritative current state of the Nautilus Developer Toolkit project.
>
> Update this document whenever a major repository, architecture, testing, release, or development milestone is completed.
>
> It is intended to help human contributors and AI assistants understand the project without reconstructing its history from individual commits or conversations.

---

# Project Information

**Project Name**

Nautilus Developer Toolkit

**Abbreviation**

NDT

**Repository Name**

`nautilus-developer-toolkit`

**Current Stable Version**

`1.0.0`

**Current Development Line**

Version 2 modular refactoring

**License**

MIT

**Project Status**

Version 1.0 is frozen and tagged.

The public GitHub repository and professional repository foundation are complete.

Version 2 modular refactoring is in progress on feature branches while preserving the Version 1 behavior and frozen snapshot.

---

# Project Objective

Develop a professional, production-quality, open-source Linux developer toolkit implemented as a Nautilus Python extension.

The toolkit provides context-aware developer actions directly from the Nautilus right-click menu.

Primary goals:

* Improve Linux developer productivity.
* Detect project types and development environments automatically.
* Provide context-aware actions for common development workflows.
* Integrate editors, terminals, Python tools, Git, Docker, local AI services, and hardware utilities.
* Preserve a Linux-first design.
* Preserve a local-first design.
* Keep AI and cloud integrations optional.
* Maintain compatibility with the stable Version 1 behavior.
* Support long-term modular development and community contributions.

---

# Local Development Environment

**Repository location**

```text
/home/ecube/Projects/nautilus-developer-toolkit
```

**Installed working Nautilus extension**

```text
~/.local/share/nautilus-python/extensions/developer_context_menu.py
```

**Primary development source**

```text
developer_context_menu.py
```

**Frozen Version 1 snapshot**

```text
snapshots/developer_context_menu_v1.0.0_snapshot.py
```

The installed extension and frozen Version 1 snapshot were SHA256-verified before Version 2 development began.

The frozen snapshot is the authoritative Version 1 baseline and must not be modified.

**Development platform**

* Ubuntu 24.04 LTS
* GNOME desktop
* Nautilus file manager
* Python 3.11+
* VSCodium
* gedit
* PyCharm

---

# Repository

**Public GitHub repository**

```text
https://github.com/aimldstejas/nautilus-developer-toolkit
```

**Repository visibility**

Public

**Default stable branch**

```text
main
```

**Integration branch**

```text
develop
```

**Version 2 architecture branch created during initial modularization**

```text
feature/v2-modular-architecture
```

**Current utility-extraction development branch**

```text
feature/v2-utils-extraction
```

**Stable release tag**

```text
v1.0.0
```

**Branch protection**

The `main` branch is protected.

Changes intended for the stable branch should be developed on feature branches, reviewed, and integrated through the established branch workflow.

---

# Development Philosophy

The project follows this engineering sequence:

```text
Vision
  ↓
Architecture
  ↓
Documentation
  ↓
Engineering Standards
  ↓
Repository Infrastructure
  ↓
Version Control
  ↓
Refactoring
  ↓
Testing
  ↓
Release
```

The project does not begin with a rewrite of the working extension.

Instead, the stable implementation is preserved while responsibilities are extracted incrementally into testable modules.

Every refactoring step should:

1. Preserve existing user-visible behavior.
2. Move only a controlled and reviewable responsibility.
3. Add or update tests for the extracted behavior.
4. Pass repository quality checks.
5. Be committed as a focused change.
6. Keep the frozen Version 1 snapshot unchanged.

---

# Version 1 Status

Version 1.0 represents the stable baseline of the original implementation.

## Version 1 State

* Stable
* Frozen
* Documented
* Committed to Git
* Published to GitHub
* Tagged as `v1.0.0`
* Preserved through a verified snapshot

Version 1 remains a monolithic implementation by design.

The monolithic architecture is a known limitation, not a reason to modify the frozen snapshot.

Version 2 development must preserve Version 1 behavior wherever practical.

---

# Version 1 Features

The Version 1 extension already provides the following capabilities.

## Developer Context Menu

* Native Nautilus right-click integration
* Context-aware menu construction
* Folder and project actions
* Project detection and environment-aware actions

## Editors

* Open gedit Here
* Open VSCodium Here
* Open PyCharm Here

## Terminal

* Open Terminal Here

## Python Support

* Python project detection
* Virtual environment detection
* Conda environment detection
* Environment activation support
* IPython launcher
* Jupyter Notebook launcher
* JupyterLab launcher
* Streamlit application support
* FastAPI application support

## Git Integration

* Git repository detection
* Repository status
* Current branch information
* Remote repository information
* Fetch
* Pull
* Push
* Git log viewer

## Docker Integration

* Docker project detection
* Docker Compose Up
* Docker Compose Down
* Docker Compose Restart
* Docker logs
* Container information
* Image information
* Docker disk-usage information

## Local AI Integration

* Ollama launcher
* Ollama model listing
* Ollama model build support
* Dify launcher
* Open WebUI launcher
* BentoPDF launcher

## GPU and CUDA Utilities

* NVIDIA GPU information
* CUDA information

## Smart Project Detection

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

## Project Actions

* Project identification
* Environment activation
* Streamlit execution
* FastAPI execution
* FastAPI documentation launcher
* Docker Compose controls
* Ollama model build support

## Project Wizard

Project templates include:

* Basic Python
* Data Science
* Streamlit
* FastAPI
* Docker
* Retrieval-Augmented Generation
* AI Agent
* Model Context Protocol server

The Project Wizard supports:

* Project-directory creation
* Template generation
* Virtual-environment creation
* Dependency installation
* Editor launch
* Sequential project setup
* Automatic application startup where applicable

---

# Repository Foundation

The professional repository foundation is complete.

## Root Documentation and Configuration

```text
README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
DEVELOPMENT_GUIDELINES.md
ROADMAP.md
ARCHITECTURE.md
SECURITY.md
SUPPORT.md
CODE_OF_CONDUCT.md
PROJECT_CONTEXT.md
VERSION
pyproject.toml
requirements.txt
.gitignore
```

## Documentation Directory

```text
docs/
├── INSTALLATION.md
├── QUICK_START.md
├── USER_GUIDE.md
├── FAQ.md
├── TROUBLESHOOTING.md
├── CONFIGURATION.md
├── PROJECT_WIZARD.md
├── AI_INTEGRATION.md
├── DOCKER.md
├── GIT.md
├── PYTHON.md
└── CHANGELOG_GUIDE.md
```

## Additional Repository Areas

```text
.github/
assets/
docs/
screenshots/
scripts/
snapshots/
src/
tests/
```

GitHub issue templates, pull-request guidance, contributor documentation, security guidance, and support documentation are present.

---

# Version 2 Architectural Direction

Version 2 replaces the monolithic development model with an incremental modular architecture.

The refactor is being performed by extraction rather than wholesale replacement.

## Current Package Root

```text
src/nautilus_developer_toolkit/
```

## Current Modular Areas

```text
src/nautilus_developer_toolkit/
├── integrations/
├── services/
└── utils/
```

Additional architectural areas may be introduced as responsibilities are extracted.

## Service Layer

The service layer contains modules for responsibilities such as:

```text
services/
├── ai_service.py
├── conda_service.py
├── cuda_service.py
├── docker_service.py
├── exceptions.py
├── git_service.py
├── project_service.py
├── streamlit_service.py
├── terminal_service.py
└── vscode_service.py
```

These modules establish boundaries between Nautilus menu presentation and the underlying development-tool operations.

## Integration Layer

The integration layer contains optional external or local-service integrations:

```text
integrations/
├── bentopdf.py
├── dify.py
├── ollama.py
└── openwebui.py
```

These integrations must remain optional and must not make the core Nautilus extension dependent on AI services.

## Utility Layer

The first controlled utility extraction has begun.

Low-dependency filesystem and path helpers have been moved from the monolithic extension into reusable utility modules under:

```text
src/nautilus_developer_toolkit/utils/
```

The corresponding unit tests include:

```text
tests/unit/test_filesystem_utils.py
tests/unit/test_path_utils.py
```

This extraction is intentionally limited to low-dependency helpers so that functionality can be moved safely before higher-level menu, service, and project-detection logic.

---

# Testing and Quality Tooling

A testing and static-analysis foundation is now present.

## Pytest

* Pytest scaffolding has been created.
* Unit tests have been added for extracted utilities.
* The current test suite contains 10 tests.
* The current test suite passes.

## Ruff

Ruff is used for Python linting and code-quality checks.

The current Ruff lint checks pass for the configured project scope.

The original monolithic `developer_context_menu.py` may still be reported by `ruff format --check` as requiring reformatting.

A wholesale formatting-only rewrite of the monolithic file should not be mixed into functional extraction commits. Formatting changes should be controlled and reviewed separately.

## Mypy

Mypy is configured for static type checking.

The current type-checking run succeeds with no reported issues across the checked source files.

GNOME and Nautilus `gi` bindings may expose dynamically typed interfaces, so practical exceptions may be required where complete third-party typing information is unavailable.

## Pre-commit

Pre-commit hooks are configured.

Checks include repository hygiene such as:

* Large-file detection
* Case-conflict detection
* Merge-conflict detection
* TOML validation
* YAML validation
* End-of-file fixes
* Mixed-line-ending detection
* Trailing-whitespace detection

The configured checks have passed for the committed Version 2 extraction work.

---

# Current Git and Development Status

## Completed

* Git repository initialized.
* Public GitHub repository created.
* Initial repository foundation committed.
* `main` branch created and protected.
* `develop` branch created.
* Version `1.0.0` tagged as `v1.0.0`.
* Stable Version 1 snapshot preserved.
* Version 2 feature development started.
* Initial modular package structure created.
* Service modules introduced.
* Optional integration modules introduced.
* Test scaffolding created.
* Ruff configured and used.
* Mypy configured and used.
* Pre-commit checks configured and used.
* Filesystem utility extraction completed.
* Path utility extraction completed.
* Unit tests added for the extracted utilities.
* Latest utility-extraction work committed and pushed.

## In Progress

* Incremental extraction of responsibilities from `developer_context_menu.py`
* Expansion of unit-test coverage
* Refinement of module boundaries
* Reduction of coupling between Nautilus presentation logic and operational logic

## Intentionally Deferred

* GitHub Actions and CI workflows
* Distribution packaging
* Linux package publication
* Plugin SDK
* User-facing configuration system
* Full menu-layer extraction
* Full detector-layer extraction
* Version 2 release preparation

CI/CD files should remain deferred until the local architecture and test foundation are sufficiently stable.

---

# Current Working Branch and Refactoring Strategy

The current extraction work is associated with:

```text
feature/v2-utils-extraction
```

The immediate refactoring strategy is:

1. Inspect `developer_context_menu.py`.
2. Identify the lowest-dependency helper functions.
3. Extract filesystem and path logic first.
4. Preserve public behavior and call signatures where practical.
5. Add focused unit tests.
6. Run linting, type checking, tests, and pre-commit checks.
7. Commit one coherent extraction at a time.
8. Continue toward progressively higher-level responsibilities.

High-coupling menu and Nautilus integration logic should not be extracted before its lower-level dependencies are stable.

---

# Planned Version 2 Package Direction

The long-term Version 2 architecture may evolve toward:

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

The exact structure should be introduced incrementally.

Directories must not be created merely to match a theoretical architecture. Each module or directory should correspond to a real responsibility with clear ownership and tests where practical.

---

# Engineering Standards

The project follows these standards:

* Python 3.11+
* PEP 8
* Semantic Versioning
* Type hints where practical
* Focused modules
* Single Responsibility Principle
* Composition preferred over inheritance
* Readability over cleverness
* Backward compatibility whenever practical
* Local-first operation
* Linux-first development
* Optional AI integrations
* Optional cloud integrations
* Small, reviewable commits
* Tests for extracted behavior
* No unrelated changes in refactoring commits

---

# Branching and Commit Principles

## Stable Branch

```text
main
```

The stable branch represents reviewed and releasable project history.

## Integration Branch

```text
develop
```

The integration branch is used to combine completed development work before stable release preparation.

## Feature Branches

Feature branches should be narrowly scoped.

Examples:

```text
feature/v2-modular-architecture
feature/v2-utils-extraction
```

## Commit Principles

Commits should:

* Represent one coherent change.
* Use clear conventional-style messages where practical.
* Avoid mixing formatting, feature development, and architectural refactoring.
* Include relevant tests.
* Pass configured checks before being pushed.
* Preserve the frozen Version 1 snapshot.

---

# Known Limitations

Current limitations include:

* The main Nautilus extension remains substantially monolithic.
* Not all menu actions have been moved into services.
* Project detectors have not yet been fully separated.
* Menu construction has not yet been fully modularized.
* The configuration system is not yet available.
* The plugin architecture is not yet available.
* Test coverage is still limited to the earliest extracted components.
* GitHub Actions CI/CD has not yet been introduced.
* Linux distribution packaging has not yet been implemented.
* Some dynamic GNOME and Nautilus APIs have incomplete static typing.
* The monolithic source has not yet undergone a dedicated formatting pass.

These are expected development-stage limitations and should be addressed incrementally.

---

# Immediate Next Milestones

1. Review the remaining helper functions in `developer_context_menu.py`.

2. Identify the next lowest-dependency extraction candidates.

3. Avoid extracting high-coupling Nautilus menu logic prematurely.

4. Add unit tests before or alongside each extraction.

5. Run the full local quality sequence after every milestone:

```text
ruff check
mypy
pytest
pre-commit
```

6. Commit and push each coherent extraction independently.

7. Update `PROJECT_CONTEXT.md` and `CHANGELOG.md` after significant architectural milestones.

8. Keep GitHub Actions and CI workflow creation deferred until the local modular architecture and test suite are sufficiently mature.

---

# Long-Term Roadmap

## Version 1.x

* Stable baseline maintenance
* Bug fixes
* Documentation corrections
* Compatibility fixes
* Packaging preparation
* Additional regression tests

## Version 2.0

* Modular architecture
* Separation of presentation and operational logic
* Dedicated detectors
* Dedicated services
* Reusable utilities
* Configuration system
* Expanded automated tests
* Stable package interfaces
* Backward-compatible migration from the Version 1 implementation

## Version 2.5

* Plugin architecture
* Plugin discovery and registration
* Docker plugin
* Git plugin
* AWS plugin
* Ollama plugin
* Dify plugin
* Contributor-facing plugin documentation

## Version 3.x

* AI Project Generator
* Repository Chat
* Repository Explanation
* AI Code Review
* Automatic Documentation
* Traceback Analysis
* Log Analysis
* AI-assisted debugging
* Plugin SDK
* Repository intelligence

AI functionality must remain optional and must not become a requirement for core toolkit operation.

---

# Working Rules

* Preserve working functionality whenever practical.
* Never modify the frozen Version 1 snapshot.
* Avoid unnecessary redesign.
* Complete one major milestone before beginning another.
* Extract low-dependency responsibilities before high-coupling components.
* Prefer maintainability over rapid feature addition.
* Prefer explicit code over clever abstractions.
* Add tests for extracted behavior.
* Keep feature branches focused.
* Do not combine unrelated changes in one commit.
* Do not introduce GitHub Actions until the deferred CI milestone begins.
* Do not add mandatory cloud or AI dependencies.
* Update this document whenever the authoritative project state changes.

---

# Last Updated

**Date:** 2026-07-28

**Milestone:** Version 1.0 frozen and published; Version 2 modular architecture and utility extraction in progress.
