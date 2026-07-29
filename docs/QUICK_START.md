# Quick Start

The stable public release is Version `1.0.0` at tag `v1.0.0`. The modular path below installs unreleased Version 2 development at `2.0.0.dev0` from `develop`.

For stable Version 1, follow the tagged single-file procedure in [Installation](INSTALLATION.md).

## Version 2 Development

```bash
git clone --branch develop \
  https://github.com/aimldstejas/nautilus-developer-toolkit.git

cd nautilus-developer-toolkit

/usr/bin/python3 -m pip install \
  --user \
  --break-system-packages \
  .

install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

nautilus -q

/usr/bin/python3 -c \
  "import gi, nautilus_developer_toolkit; print(nautilus_developer_toolkit.__file__)"
```

Nautilus loads extensions through system Python. Use `/usr/bin/python3`, not an active Conda interpreter, so the modular package is available at runtime. Reopen Nautilus and right-click inside a folder to verify the menu manually.

See [Installation](INSTALLATION.md) for complete setup and [Migration Guide](MIGRATION_GUIDE.md) for backup, migration, upgrade, rollback, uninstall, and Version 1 restoration.
