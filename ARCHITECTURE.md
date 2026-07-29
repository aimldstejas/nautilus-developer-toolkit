# Architecture

This document describes the architectural design of Nautilus Developer Toolkit (NDT).

---

# Current Architecture (Version 2 Development)

Version 1.0.0 remains the frozen baseline. Version 2 development now includes a focused reusable utility layer while `developer_context_menu.py` continues to provide the Nautilus extension entry point.

## Nautilus Integration and Orchestration

`DeveloperContextMenu` primarily handles Nautilus integration, menu construction, UI presentation, notifications, terminal and process workflows, and project-action coordination.

Thin compatibility wrappers remain for extracted utilities where they preserve existing class-level behavior and verified call sites. These wrappers keep `DeveloperContextMenu` as the integration boundary without duplicating reusable implementation logic.

The remaining substantial class methods are predominantly orchestration or UI-bound. Further extraction is not automatically beneficial when it would fragment coordinated workflows.

## Reusable Utility Layer

Reusable non-UI logic resides under `src/nautilus_developer_toolkit/utils/`.

```text
utils/
    command_utils.py
    conda_utils.py
    docker_utils.py
    filesystem.py
    git_utils.py
    menu_utils.py
    notification_utils.py
    paths.py
    process_utils.py
    project_utils.py
```

The utility layer contains focused responsibilities for command discovery, Conda operations, Docker Compose detection, filesystem helpers, Git helpers, menu-item construction, notifications, path conversion, process launching, and project detection.

`project_utils.py` contains project-root detection, project detection, and project-report formatting.

Utility modules avoid direct Nautilus, Gtk, and GObject dependencies. The exceptions are deliberate boundary patterns where a utility accepts an injected factory or callback, such as menu-item construction or process-launch notification handling.

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
