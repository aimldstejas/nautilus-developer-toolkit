# Installation

Nautilus Developer Toolkit currently has two distinct deployment paths. Stable Version 1 is a tagged single-file extension. Version 2 on `develop` is the unreleased `2.0.0rc1` release candidate and requires both the modular Python package and the repository-root extension entrypoint. It has not been tagged or published and is not the stable Version 2 release.

## Requirements

- Linux with GNOME and Nautilus
- Python 3.11 or newer
- `nautilus-python` or the distribution-equivalent Nautilus Python bindings
- PyGObject and the applicable GNOME bindings
- Git for source checkout and tagged Version 1 restoration

## Stable Version 1 Installation

Version `1.0.0` at tag `v1.0.0` is the stable public release. It uses the tagged single-file `developer_context_menu.py` and does not require the modular `nautilus_developer_toolkit` package.

Clone the stable tag and install its entrypoint:

```bash
git clone --branch v1.0.0 \
  https://github.com/aimldstejas/nautilus-developer-toolkit.git

cd nautilus-developer-toolkit

install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

nautilus -q
```

Launch Nautilus again and verify that the Developer Toolkit context menu appears.

## Version 2 Release-Candidate Installation

> Warning: `develop` contains the unreleased `2.0.0rc1` Version 2 release candidate. No release-candidate tag or GitHub release exists; use the stable `v1.0.0` installation above unless you are intentionally evaluating the release-candidate branch state.

### Clone `develop`

```bash
git clone --branch develop \
  https://github.com/aimldstejas/nautilus-developer-toolkit.git

cd nautilus-developer-toolkit
```

### Back Up an Existing Extension

```bash
extension_path="$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

if [ -f "$extension_path" ]; then
  cp "$extension_path" \
    "${extension_path}.backup.$(date +%Y%m%d-%H%M%S)"
fi
```

Keep the backup until the Version 2 release candidate has been validated in Nautilus.

### Install the Modular Package for Nautilus

Nautilus loads Python extensions through its system Python runtime, not through an active Conda environment. Install the package into the user site visible to `/usr/bin/python3`:

```bash
/usr/bin/python3 -m pip install \
  --user \
  --break-system-packages \
  .
```

Do not use `pip install -r requirements.txt` when `requirements.txt` is absent.

### Deploy the Extension Entrypoint

The repository-root `developer_context_menu.py` is the active Nautilus extension entrypoint.

```bash
install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"
```

### Restart and Validate

```bash
nautilus -q
```

Validate that system Python can import both the GNOME bindings and the package:

```bash
/usr/bin/python3 -c \
  "import gi, nautilus_developer_toolkit; print(nautilus_developer_toolkit.__file__)"
```

Launch Nautilus, right-click inside a folder, and confirm that the Developer Toolkit menu appears and representative actions behave as expected. The import check alone is not a Nautilus runtime test.

## Migration, Rollback, and Uninstall

For complete backup, upgrade, rollback, package uninstall, and deterministic Version 1 restoration procedures, see the [Version 1 to Version 2 Release Candidate Migration Guide](MIGRATION_GUIDE.md).

For failures involving imports, missing menu entries, or Nautilus logs, see [Troubleshooting](TROUBLESHOOTING.md).
