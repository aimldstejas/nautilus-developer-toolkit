# Nautilus Developer Toolkit Roadmap

This roadmap separates completed engineering from release-readiness work and future product development. Version 2 remains unreleased development at `2.0.0.dev0`.

## Stable Version 1 Maintenance

Version `1.0.0` at tag `v1.0.0` remains the stable public release and the `main` branch remains the stable Version 1 boundary.

Completed and continuing responsibilities:

- Preserve the frozen Version 1 snapshot byte-for-byte.
- Maintain user support, compatibility guidance, and targeted fixes for the stable baseline.
- Keep Version 1 deployment available as the tagged single-file Nautilus extension.

GitHub currently marks the `v1.0.0` release as a pre-release. This is an external metadata error; the tag and verified snapshot remain the stable Version 1 boundary. Correcting the flag is a separate pending task.

## Version 2.0 Development

### Completed Engineering

- [x] Modular package architecture under `src/nautilus_developer_toolkit/`.
- [x] Reusable utility extraction and compatibility wrappers.
- [x] Integration of the Version 2 architecture and extracted utilities into `develop`.
- [x] Unit-test baseline of `96` passing tests.
- [x] Ruff, mypy, pytest, pre-commit, and GitHub Actions quality checks.
- [x] Frozen Version 1 snapshot restoration and integrity verification.
- [x] Removal and ignore policy for generated Graphify output.
- [x] Alignment of `VERSION` and package metadata at `2.0.0.dev0`.
- [x] Modern SPDX license metadata and explicit license-file packaging.
- [x] Warning-free isolated wheel and source-distribution validation.
- [x] Disposable wheel installation and package-import validation.
- [x] Release, installation, and Version 1-to-Version 2 development migration documentation.

### Current Release Readiness

- [ ] Correct the external GitHub `v1.0.0` pre-release flag.
- [x] Protect `main` with the active repository ruleset `Protect main` (ID `19731984`).
- [ ] Validate a clean system-Python package installation and Nautilus extension deployment.
- [ ] Confirm manual Nautilus menu behavior, rollback, uninstall, and Version 1 restoration.

The default branch, `main`, is protected by the active repository ruleset `Protect main` (ID `19731984`). Changes require a pull request, successful `quality`, `tests (3.11)`, and `tests (3.12)` checks, resolved review conversations, and an up-to-date branch. Only normal merge commits are allowed; force-pushes and branch deletion are blocked.

### Future Release Candidate

After release-readiness work is complete, prepare a Version 2 release candidate in a separate controlled task. That phase should align release-candidate metadata and release notes, rerun package and deployment validation, and exercise the controlled `develop` to `main` review path. No Version 2 release candidate currently exists.

### Future Stable Version 2

A stable Version 2 release depends on successful release-candidate validation, an approved pull request into protected `main`, post-merge verification, a stable version decision, tagging, release publication, and post-release checks.

Remaining product-level work that need not block the initial Version 2 release should be prioritized separately, including configuration-system evolution, cleaner APIs where beneficial, orchestration review, UI-bound workflow improvements, and project-template maturity.

## Version 2.5

### Goal

Develop an optional plugin ecosystem after Version 2 stability. Potential integrations include Docker, Git, Ollama, Dify, Kubernetes, and AWS plugins.

## Version 3.0

### Goal

Explore optional AI-assisted development capabilities, including repository explanation, review assistance, test and documentation generation, traceback and log analysis, and assisted refactoring. AI functionality must not become a requirement for the core toolkit.

## Long-Term Vision

Grow Nautilus Developer Toolkit into a broader Linux developer platform while keeping the Nautilus extension as the primary interface. Possible later components include a command-line interface, desktop application, editor integrations, an MCP server, and optional local AI agents.
