# Nautilus Developer Toolkit Project Context

This document records durable project state and release boundaries. Update it when a major repository, architecture, testing, packaging, or release milestone changes.

**Last updated:** `2026-07-29`

## Project Information

- **Repository:** `aimldstejas/nautilus-developer-toolkit`
- **Repository root:** `$HOME/Projects/nautilus-developer-toolkit`
- **Current stable public version:** `1.0.0`
- **Stable tag:** `v1.0.0`
- **Current Version 2 development version:** `2.0.0.dev0`
- **License:** MIT
- **Primary platform:** Linux, GNOME, Nautilus, and Python 3.11 or newer

Version 2 is unreleased development. It must not be described as a stable release.

## Project Objective

Nautilus Developer Toolkit is a Nautilus Python extension that exposes context-aware developer actions through the file manager. It aims to reduce repetitive terminal setup while keeping automation visible and understandable.

Core goals include:

- Detecting projects and development environments.
- Providing editor, terminal, Python, Git, Docker, and project actions.
- Keeping optional AI and local-service integrations separate from the core toolkit.
- Preserving stable Version 1 behavior while evolving a maintainable Version 2 architecture.
- Supporting focused testing, packaging, and community contributions.

## Stable Version 1 Boundary

Version `1.0.0` is the stable, frozen baseline. It is represented by:

- the `main` branch at the stable Version 1 boundary;
- the `v1.0.0` Git tag;
- the tagged single-file `developer_context_menu.py`; and
- `snapshots/developer_context_menu_v1.0.0_snapshot.py`, which is byte-for-byte identical to the tagged Version 1 snapshot.

The frozen snapshot is immutable release evidence and must not be refactored, formatted, or adapted for Version 2.

GitHub currently marks the `v1.0.0` release as a pre-release. This is an external metadata error; the `v1.0.0` tag and verified snapshot remain the stable Version 1 boundary. Correcting the flag is a separate pending task.

## Branch Roles and Governance

- `main` is the stable Version 1 boundary and eventual stable-release branch.
- `develop` contains integrated Version 2 development and release-readiness work.
- Focused feature and integration branches preserve development history and should not be deleted until release and rollback needs are resolved.

The default branch, `main`, is protected by the active repository ruleset `Protect main` (ID `19731984`). Changes require a pull request, successful `quality`, `tests (3.11)`, and `tests (3.12)` checks, resolved review conversations, and an up-to-date branch. Only normal merge commits are allowed; force-pushes and branch deletion are blocked.

## Version 1 Feature Inventory

The stable Version 1 extension includes:

- Nautilus developer context menus for folders and supported files.
- Editor and terminal launch actions.
- Python virtual-environment, package, test, formatting, and analysis helpers.
- Git repository, branch, status, log, fetch, pull, push, diff, and maintenance actions.
- Docker and Docker Compose actions.
- Project detection for common languages, frameworks, and environment markers.
- Project reporting, cleanup, archive, backup, and wizard workflows.
- Optional Ollama, Dify, GPU, and CUDA utilities.

This inventory is historical product context, not a claim that every optional integration is available on every host.

## Version 2 Architecture

Version 2 evolves the single-file design incrementally instead of replacing it wholesale. The active development line includes:

```text
developer_context_menu.py
src/nautilus_developer_toolkit/
├── __init__.py
├── integrations/
├── services/
└── utils/
```

The repository-root `developer_context_menu.py` remains the Nautilus extension entrypoint and the boundary for menu presentation, Nautilus integration, and coordinated UI workflows. Reusable non-UI responsibilities have been extracted into focused package modules with compatibility wrappers where needed.

Completed architectural work includes:

- modular package foundations;
- utility extraction for command, filesystem, path, notification, Conda, process, Git, Docker Compose, menu-item, project-root, project-detection, and project-report responsibilities;
- integration of that work into `develop`; and
- preservation of verified call sites and user-facing behavior through compatibility boundaries.

Additional extraction is not automatically desirable when it would fragment cohesive Nautilus workflows.

## Testing and Quality

The current validated baseline is `96` passing unit tests. Quality tooling includes:

- pytest for focused unit tests;
- mypy for static type checking;
- Ruff for linting;
- pre-commit configuration; and
- active GitHub Actions workflows for tests and lint/type checks.

Recent release-readiness changes have passed both local validation and the active GitHub Actions workflows on `develop`.

## Version and Packaging State

- `VERSION` is `2.0.0.dev0`.
- `pyproject.toml` is `2.0.0.dev0`.
- `CHANGELOG.md` remains under `[Unreleased]`.
- The package uses the SPDX license expression `MIT`.
- `LICENSE` is explicitly included through package metadata.
- The build-system requirement includes `setuptools>=77.0.3`.
- Isolated wheel and source-distribution builds complete without the previous license deprecation warnings.
- A disposable wheel installation and `nautilus_developer_toolkit` import have succeeded.

These results establish packaging readiness but do not make Version 2 stable.

## Deployment Model

### Stable Version 1

Stable Version 1 is deployed from the tagged single-file `developer_context_menu.py`. It does not require the modular Python package.

### Version 2 Development

Version 2 development requires both:

1. installation of the `nautilus-developer-toolkit` package into the user site visible to `/usr/bin/python3`; and
2. deployment of the repository-root `developer_context_menu.py` to `$HOME/.local/share/nautilus-python/extensions/`.

Nautilus uses system Python, so installation and import validation must use `/usr/bin/python3`, not an active Conda interpreter. The complete procedures are maintained in `docs/INSTALLATION.md` and `docs/MIGRATION_GUIDE.md`.

## Graphify Policy

Graphify is optional contributor tooling. Generated output under `graphify-out/` was removed from tracking and is ignored. Configuration and assistant guidance remain tracked, but generated graphs must not be assumed to exist or be regenerated without explicit approval. Graphify is not part of user installation or migration.

## Current Release-Readiness State

Completed:

- Version 2 modular architecture and utility extraction integrated into `develop`.
- Frozen Version 1 snapshot restored and verified.
- Generated Graphify output removed and ignored.
- Active repository ruleset `Protect main` (ID `19731984`) configured for the default branch, `main`.
- Version metadata aligned at `2.0.0.dev0`.
- Packaging license metadata modernized.
- Wheel, source distribution, and disposable installation validated.
- Release, installation, roadmap, project-context, and migration documentation aligned.

Remaining controlled tasks:

1. Correct the external GitHub `v1.0.0` pre-release flag.
2. Perform a clean system-Python installation and Nautilus deployment validation.
3. Prepare and validate a future Version 2 release candidate.
4. Open and review a controlled `develop` to `main` pull request using normal merge history.
5. Complete stable Version 2 tagging, release publication, and post-release verification only after all approval gates pass.

## Engineering and Release Rules

- Preserve `main` and `v1.0.0` as the stable Version 1 boundary until a controlled Version 2 release transition.
- Keep Version 2 work on `develop` or focused branches until review and validation are complete.
- Prefer normal commits and reviewable pull requests; do not squash, rebase shared history, or force-push without an explicit policy change.
- Keep commits focused and avoid mixing code, documentation, packaging, and release operations without an approved reason.
- Preserve the frozen Version 1 snapshot.
- Do not regenerate or commit Graphify output automatically.
- Treat release tags, GitHub releases, branch protection, and branch cleanup as separate controlled operations.
- Keep optional AI functionality nonessential to core toolkit operation.

## Later Product Direction

After Version 2 release readiness, later work may include configuration improvements, plugin discovery and registration, additional integrations, broader distribution support, and optional AI-assisted development. Those goals must remain separate from the current release boundary and must not delay essential integrity, packaging, deployment, and governance work.
