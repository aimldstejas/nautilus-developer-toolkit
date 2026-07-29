# Migrating from Version 1 to Version 2 Development

## Scope and Status

This guide is for users intentionally evaluating unreleased Version 2 development at `2.0.0.dev0` on `develop`. Stable Version `1.0.0` remains available at tag `v1.0.0`. Version 2 is not yet a stable release.

## Deployment Models

### Stable Version 1

Version 1 uses the tagged single-file `developer_context_menu.py`. It does not require the modular Python package.

### Version 2 Development

Version 2 requires both:

- the `nautilus-developer-toolkit` package installed into the user site visible to `/usr/bin/python3`; and
- the repository-root `developer_context_menu.py` deployed to the Nautilus extension directory.

## Prerequisites

Before migrating, confirm that the host has:

- Linux with GNOME and Nautilus;
- Python 3.11 or newer;
- `nautilus-python` or equivalent Nautilus Python bindings;
- PyGObject and applicable GNOME bindings; and
- Git.

Close important Nautilus file operations before restarting Nautilus.

## Back Up the Installed Version 1 Extension

```bash
extension_path="$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

if [ -f "$extension_path" ]; then
  cp "$extension_path" \
    "${extension_path}.backup.$(date +%Y%m%d-%H%M%S)"
fi
```

Record the backup filename and retain it until migration validation is complete.

## Clone Version 2 Development

```bash
git clone --branch develop \
  https://github.com/aimldstejas/nautilus-developer-toolkit.git

cd nautilus-developer-toolkit
```

If the repository is already cloned, verify that the intended checkout is `develop` and that local work will not be overwritten before updating it.

## Install the Version 2 Package

Nautilus uses system Python rather than an active Conda interpreter. Install the package with `/usr/bin/python3`:

```bash
/usr/bin/python3 -m pip install \
  --user \
  --break-system-packages \
  .
```

## Deploy the Version 2 Entrypoint

```bash
install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"
```

## Restart Nautilus

```bash
nautilus -q
```

Launch Nautilus again after the existing process exits.

## Validate the Migration

Validate system-Python imports:

```bash
/usr/bin/python3 -c \
  "import gi, nautilus_developer_toolkit; print(nautilus_developer_toolkit.__file__)"
```

Then validate the Nautilus integration manually:

1. Open Nautilus.
2. Right-click inside a representative project folder.
3. Confirm that the Developer Toolkit menu appears.
4. Exercise only safe representative actions appropriate to the host.
5. Review Nautilus logs using the procedures in [Troubleshooting](TROUBLESHOOTING.md) if the menu or imports fail.

The Python import check validates package visibility; it does not replace the manual Nautilus menu test.

## Upgrade an Existing Version 2 Development Installation

From a clean local `develop` checkout, fetch and review the incoming changes before updating. After updating to an approved commit, reinstall the package and redeploy the entrypoint using the same installation commands:

```bash
/usr/bin/python3 -m pip install \
  --user \
  --break-system-packages \
  .

install -Dm 0644 developer_context_menu.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

nautilus -q
```

Repeat import and manual menu validation after every development upgrade.

## Roll Back with the Retained Backup

List the retained backups and verify the exact file before restoring it:

```bash
extension_dir="$HOME/.local/share/nautilus-python/extensions"
find "$extension_dir" -maxdepth 1 -type f \
  -name 'developer_context_menu.py.backup.*' -print
```

After reviewing the list, the following command selects the newest timestamped backup and prints its path before restoring it:

```bash
extension_path="$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"
backup_path="$(find "$HOME/.local/share/nautilus-python/extensions" \
  -maxdepth 1 -type f \
  -name 'developer_context_menu.py.backup.*' -print | sort | tail -n 1)"

if [ -z "$backup_path" ]; then
  printf 'No extension backup was found.\n' >&2
  exit 1
fi

printf 'Restoring backup: %s\n' "$backup_path"
install -Dm 0644 "$backup_path" "$extension_path"
nautilus -q
```

The command selects the newest timestamped backup created by this guide and prints the selected path before restoration. If that is not the intended backup, stop and use deterministic tagged restoration instead.

## Restore Version 1 Deterministically from `v1.0.0`

Run this from the repository checkout:

```bash
git show v1.0.0:developer_context_menu.py \
  > /tmp/developer_context_menu_v1.0.0.py

install -Dm 0644 /tmp/developer_context_menu_v1.0.0.py \
  "$HOME/.local/share/nautilus-python/extensions/developer_context_menu.py"

rm -f /tmp/developer_context_menu_v1.0.0.py
nautilus -q
```

This restores the tagged stable Version 1 entrypoint without changing the working branch.

## Uninstall the Version 2 Package

After restoring or removing the extension entrypoint, uninstall the modular package if it is no longer needed:

```bash
/usr/bin/python3 -m pip uninstall \
  --break-system-packages \
  -y nautilus-developer-toolkit
```

Do not uninstall shared GNOME or Nautilus Python dependencies.

## Validate After Rollback

After restarting Nautilus:

1. Confirm that the Version 1 menu appears.
2. Confirm that representative Version 1 actions behave as expected.
3. If the Version 2 package was uninstalled, verify that the restored Version 1 entrypoint still loads without requiring it.
4. Consult [Troubleshooting](TROUBLESHOOTING.md) for Nautilus logging and extension-loading diagnostics.

## Compatibility Expectations

Version 2 preserves compatibility wrappers and has no intended behavior change for the utility-extraction phase, but it remains development software. Host behavior can vary with the Linux distribution, Nautilus and GNOME versions, system Python environment, installed developer tools, and optional integrations. Keep the stable Version 1 restoration path until Version 2 validation is complete.
