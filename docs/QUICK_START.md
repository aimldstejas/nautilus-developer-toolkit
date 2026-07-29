# Quick Start

## Install

```bash
git clone https://github.com/aimldstejas/nautilus-developer-toolkit.git
cd nautilus-developer-toolkit

/usr/bin/python3 -m pip install --user --break-system-packages .

install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

nautilus -q
```

Nautilus loads extensions through system Python. Use `/usr/bin/python3`, not an active Conda Python environment, so the modular `nautilus_developer_toolkit` package is available at runtime.

Right-click inside any folder to access the Developer Toolkit context menu.

Refer to `INSTALLATION.md` for complete installation details.
