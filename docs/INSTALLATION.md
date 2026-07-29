# Installation

## Requirements

- Linux
- Python 3.11 or newer
- Nautilus
- `python3-nautilus`

## Clone the repository

```bash
git clone https://github.com/aimldstejas/nautilus-developer-toolkit.git
cd nautilus-developer-toolkit
```

## Install the modular package for Nautilus

Nautilus loads Python extensions through its system Python runtime, not through the active Conda environment. Install the modular package into the system Python user site before deploying the extension.

On this Ubuntu setup, use `/usr/bin/python3`, not bare `python3`.

```bash
/usr/bin/python3 -m pip install --user --break-system-packages .
```

Do not use `pip install -r requirements.txt` when `requirements.txt` is absent.

## Install the extension entrypoint

The repository-root `developer_context_menu.py` file is the active Nautilus extension entrypoint. Do not use the obsolete `src/extension.py` path.

```bash
install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"
```

## Restart Nautilus

```bash
nautilus -q
```

Launch Nautilus again and verify that the Developer Toolkit context menu appears.
