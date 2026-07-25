# Troubleshooting

## Developer menu does not appear

Verify:

- `nautilus-python` is installed.
- The extension file is located in:
  `~/.local/share/nautilus-python/extensions/`
- Restart Nautilus:

```bash
nautilus -q
```

## Docker menu missing

Ensure Docker is installed and available in `PATH`.

## Git menu missing

Verify that the current folder is a Git repository.

## Python options missing

Ensure the current folder contains a supported Python project.

## AI options missing

Verify that the relevant local AI service (e.g., Ollama or Dify) is installed and running.
