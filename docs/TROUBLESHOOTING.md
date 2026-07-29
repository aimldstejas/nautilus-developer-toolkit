# Troubleshooting

## Developer menu does not appear

Verify:

- `python3-nautilus` is installed.
- The extension file is located at `~/.local/share/nautilus-python/extensions/developer_context_menu.py`.
- Restart Nautilus:

```bash
nautilus -q
```

## ModuleNotFoundError: No module named `nautilus_developer_toolkit`

This error means the extension was copied without installing the modular package into the Python environment visible to Nautilus.

Verify the system Python runtime can import both GI and the package:

```bash
/usr/bin/python3 -c "import gi, nautilus_developer_toolkit; print(nautilus_developer_toolkit.__file__)"
```

From the repository root, reinstall the package with system Python, redeploy the root extension entrypoint, and restart Nautilus:

```bash
/usr/bin/python3 -m pip install --user --break-system-packages .

install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

nautilus -q
```

Do not use an active Conda environment for Nautilus runtime deployment.

## Docker menu missing

Ensure Docker is installed and available in `PATH`.

## Git menu missing

Verify that the current folder is a Git repository.

## Python options missing

Ensure the current folder contains a supported Python project.

## AI options missing

Verify that the relevant local AI service (e.g., Ollama or Dify) is installed and running.
