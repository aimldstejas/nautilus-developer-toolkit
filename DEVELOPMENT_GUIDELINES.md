# Development Guidelines

This document defines the engineering standards, development workflow, and contribution expectations for the **Nautilus Developer Toolkit (NDT)**.

All contributors are expected to follow these guidelines to ensure the project remains maintainable, reliable, and consistent.

---

# 1. General Principles

The project prioritizes:

- Readability
- Maintainability
- Reliability
- Simplicity
- Backward compatibility

Code should always be written for humans first and computers second.

Avoid clever solutions when a simpler implementation is available.

---

# 2. Supported Environment

Current development target:

- Ubuntu 24.04 LTS
- Python 3.11+
- Nautilus
- nautilus-python

Additional Linux distributions will be validated before public releases.

---

# 3. Coding Standards

The project follows:

- PEP 8
- Meaningful variable and function names
- Type hints where practical
- Single Responsibility Principle
- Composition preferred over inheritance

Avoid:

- Unnecessary global variables
- Deep nesting
- Duplicate code
- Hard-coded paths
- Hard-coded URLs

---

# 4. Architecture

Large monolithic files are not permitted for new development.

New functionality must be placed in appropriate modules.

Planned package layout:

```
menus/
detectors/
plugins/
templates/
utils/
```

Each module should have a clearly defined responsibility.

---

# 5. Backward Compatibility

Version 1.x prioritizes stability.

Existing user workflows should not break unless there is a critical security or correctness issue.

Bug fixes are encouraged.

Breaking changes require a major version.

---

# 6. Documentation

Every public function should include:

- Purpose
- Parameters
- Return value
- Exceptions (when applicable)

Complex algorithms should include explanatory comments.

User-facing features must also be documented in the project documentation.

---

# 7. Testing

New features should include:

- Manual verification
- Regression testing
- Automated tests where practical

No feature should be merged if it breaks existing functionality.

---

# 8. Versioning

The project follows Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Examples:

```
1.0.0
1.1.0
1.2.5
2.0.0
```

---

# 9. Git Workflow

Primary branches:

```
main
develop
feature/*
```

Development occurs in feature branches.

Completed work is merged into `develop`.

Stable releases are merged into `main`.

Direct commits to release branches should be avoided.

---

# 10. Commit Messages

Use clear commit messages.

Examples:

```
Add Docker Compose menu

Improve project detection

Fix Streamlit startup race condition

Refactor project wizard

Update documentation
```

Avoid vague messages such as:

```
Update

Fix

Changes

Misc
```

---

# 11. Code Reviews

Before merging:

- Code should build successfully.
- Existing functionality should be verified.
- Documentation should be updated if required.
- New code should follow the project architecture.

---

# 12. Project Philosophy

Nautilus Developer Toolkit is designed to be:

- Native to Linux
- Local-first
- AI-optional
- Extensible
- Easy to understand
- Easy to maintain

Every contribution should move the project toward these goals.
