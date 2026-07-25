# Installation

## Requirements

- Linux
- Python 3.11 or newer
- Nautilus
- nautilus-python

## Clone the repository

```bash
git clone https://github.com/<username>/nautilus-developer-toolkit.git
cd nautilus-developer-toolkit
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install the extension

Copy the extension to the Nautilus extensions directory:

```bash
mkdir -p ~/.local/share/nautilus-python/extensions
cp src/extension.py ~/.local/share/nautilus-python/extensions/
```

Restart Nautilus:

```bash
nautilus -q
```

Launch Nautilus again and verify that the Developer Toolkit context menu appears.
