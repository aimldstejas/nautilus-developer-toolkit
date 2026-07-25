# Nautilus Developer Toolkit (NDT)

> Transform the Linux file manager into a powerful developer workspace.

**Nautilus Developer Toolkit (NDT)** is an open-source Nautilus extension that brings software development, project management, container tooling, and local AI workflows directly into the Linux file manager.

Instead of repeatedly opening terminals, changing directories, or remembering commands, developers can simply **right-click inside a project folder** and launch the appropriate tools.

---

# Why NDT?

Modern developers constantly switch between:

- Terminal
- IDE
- Git
- Docker
- Python environments
- Local AI services
- Project generators

Most of these tasks begin with the same repetitive steps:

- Open terminal
- Change directory
- Activate environment
- Run command
- Wait
- Open browser

NDT removes much of this repetitive work by exposing project-aware actions directly from the Nautilus context menu.

---

# Key Features

## Smart Project Detection

Automatically detects common project types, including:

- Git repositories
- Python projects
- Virtual environments
- Conda environments
- Docker projects
- Streamlit applications
- FastAPI applications
- Jupyter projects
- Ollama Modelfiles

Context menus automatically adapt to the detected project.

---

## Editor Integration

Launch supported editors directly from Nautilus.

Current integrations include:

- VSCodium
- PyCharm
- gedit
- GNOME Terminal

---

## Python Development

Quick access to common Python workflows.

Features include:

- Environment-aware terminals
- Conda environment detection
- IPython
- Jupyter Notebook
- JupyterLab

---

## Git Integration

Common Git operations directly from Nautilus.

Examples include:

- Status
- Log
- Fetch
- Pull
- Push
- Branch information
- Repository root
- Remote repository

---

## Docker Integration

Manage containerized projects without opening a terminal.

Current actions include:

- Compose Up
- Compose Down
- Compose Restart
- View Logs
- List Containers
- List Images
- Docker Disk Usage

---

## Local AI Integration

NDT can integrate with locally hosted AI tools.

Current integrations include:

- Ollama
- Dify
- Open WebUI
- BentoPDF

Additional utilities include:

- NVIDIA GPU status
- CUDA information
- Installed Ollama models

These integrations are optional.

Core functionality does not depend on any AI service.

---

## Project Actions

Project-specific actions become available automatically.

Examples include:

- Show detected project
- Open project terminal
- Activate environment
- Run Streamlit
- Run FastAPI
- Open FastAPI documentation
- Docker Compose Up
- Docker Compose Down
- Build Ollama model

---

## Project Wizard

The integrated Project Wizard can generate starter projects.

Current templates:

- Basic Python
- Data Science
- Streamlit
- FastAPI
- Docker Compose
- RAG Application
- Agent Application
- MCP Server

Optional setup actions include:

- Initialize Git
- Create Python virtual environment
- Create Conda environment
- Install dependencies
- Open in VSCodium
- Launch application
- Open browser after server is ready

---

# Design Philosophy

NDT follows several guiding principles.

## Native Linux

Work with Linux rather than around it.

---

## Local First

Cloud services should be optional.

---

## Productivity

Reduce repetitive development work.

---

## Transparency

Avoid hidden automation.

Generated projects should be understandable.

---

## Extensibility

The toolkit should grow through modular components rather than a single monolithic script.

---

# Planned Roadmap

## Version 1.0

Stable developer productivity extension.

Features:

- Developer menus
- Project detection
- Project Wizard
- Docker support
- Git support
- Python support
- Local AI shortcuts

---

## Version 1.1

Public release preparation.

Planned work:

- Installation scripts
- Documentation
- Screenshots
- Automated testing
- Packaging
- Compatibility testing

---

## Version 2.0

Major architectural redesign.

Goals include:

- Modular codebase
- Configuration system
- Production templates
- Improved maintainability

---

## Version 2.5

Plugin architecture.

Support for independently developed plugins.

---

## Version 3.0

AI-assisted development.

Planned capabilities include:

- AI project generation
- Repository chat
- Code review
- Test generation
- Documentation generation
- Log analysis
- Traceback analysis
- Assisted refactoring

---

# Compatibility

Current development platform:

- Ubuntu 24.04
- GNOME
- Nautilus
- Python 3
- nautilus-python

Additional distributions will be tested before the first public release.

---

# Documentation

Documentation will be available under the `docs/` directory.

Planned documentation includes:

- Installation
- Configuration
- Menu Reference
- Project Wizard
- Troubleshooting
- Development Guide

---

# Contributing

Contribution guidelines will be published before the first public release.

Areas where contributions will be welcome include:

- Documentation
- Testing
- New project templates
- Plugin development
- Compatibility improvements
- Bug fixes

---

# License

This project is planned to be released under the MIT License.

---

# Project Status

**Current Version**

1.0.0

The Version 1.0 source has been frozen before architectural refactoring begins.

Future development will preserve a stable release while Version 2.x and Version 3.x evolve independently.
