# Changelog

All notable changes to Nautilus Developer Toolkit (NDT) will be documented in this file.

The project follows [Semantic Versioning](https://semver.org/).

---

# [1.0.0] - Initial Stable Release

## Added

### Developer Menu

- Native Nautilus Developer context menu
- Editor launchers
- Terminal integration

### Python Integration

- Python project detection
- Virtual environment support
- Conda environment detection
- IPython launcher
- Jupyter Notebook launcher
- JupyterLab launcher

### Git Integration

- Git status
- Git log
- Fetch
- Pull
- Push
- Branch information
- Repository root
- Remote repository

### Docker Integration

- Docker Compose Up
- Docker Compose Down
- Docker Compose Restart
- Docker logs
- Container listing
- Image listing
- Docker disk usage

### Local AI Integration

- Ollama launcher
- Dify launcher
- Open WebUI launcher
- BentoPDF launcher
- NVIDIA GPU status
- CUDA information
- Ollama model listing

### Smart Project Detection

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

### Project Actions

- Show detected project
- Open project terminal
- Activate environment
- Run Streamlit
- Run FastAPI
- Open FastAPI documentation
- Docker Compose controls
- Build Ollama model

### Project Wizard

Supported templates:

- Basic Python
- Data Science
- Streamlit
- FastAPI
- Docker Compose
- RAG Application
- Agent Application
- MCP Server

Wizard capabilities:

- Git initialization
- Virtual environment creation
- Conda environment creation
- Dependency installation
- VSCodium launch
- Application launch
- Automatic browser opening after server readiness

---

## Changed

Initial public project documentation.

---

## Fixed

Multiple Project Wizard improvements including sequential setup and application launch.

---

## Notes

Version 1.0 represents the stable baseline before the Version 2 architectural redesign.
