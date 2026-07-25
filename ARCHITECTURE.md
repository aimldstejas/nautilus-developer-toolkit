# Architecture

This document describes the architectural design of Nautilus Developer Toolkit (NDT).

---

# Current Architecture (Version 1.x)

Version 1.x consists primarily of a single Nautilus extension.

```
developer_context_menu.py
```

This architecture was appropriate during rapid feature development but has reached the practical limit for maintainability.

Version 2 will replace this with a modular architecture.

---

# Version 2 Target Architecture

```
nautilus-developer-toolkit/

src/

    extension.py

    menus/
        editors.py
        python.py
        git.py
        docker.py
        ai.py
        projects.py
        wizard.py

    detectors/
        project_detector.py
        git_detector.py
        python_detector.py
        docker_detector.py
        framework_detector.py

    plugins/
        docker/
        git/
        ollama/
        dify/
        kubernetes/
        aws/

    templates/
        python/
        streamlit/
        fastapi/
        docker/
        rag/
        agent/

    utils/
        dialogs.py
        filesystem.py
        browser.py
        terminal.py
        subprocesses.py
        config.py

tests/

docs/

assets/

scripts/
```

---

# Design Principles

The architecture follows these principles.

## Separation of Responsibilities

Each module should have one clear responsibility.

---

## Modularity

New features should be added by creating modules rather than expanding existing files.

---

## Extensibility

Optional functionality should be implemented as plugins.

---

## Configuration

Configuration values should never be hard-coded.

Future releases will load settings from configuration files.

---

## Backward Compatibility

Version 1.x workflows should remain functional whenever practical.

Breaking changes require a major version increment.

---

## Local First

Core functionality should work without Internet connectivity.

Cloud services should remain optional.

---

## AI Optional

AI integrations enhance productivity but are not required for normal operation.

---

# Future Architecture

Version 3 is expected to introduce additional components including:

- AI-assisted project generation
- Repository indexing
- Repository chat
- Code review engine
- Local MCP integration
- Plugin SDK

These capabilities will remain separate from the core Nautilus extension to preserve stability and maintainability.
