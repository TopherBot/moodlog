# moodlog – Tiny Mood‑Tracking CLI

![CI](https://github.com/your‑handle/moodlog/actions/workflows/ci.yml/badge.svg)

## What it does
`moodlog` is a single‑binary‑style command‑line tool that lets you:
- **Add** a mood entry (e.g. `happy`, `tired`, `productive`) with an optional note.
- **List** the last N entries.
- **Stats** – show how many times each mood was logged.

All data is stored locally in a tiny JSON file (`~/.moodlog.json`). No network, no database, no external services.

## Why this project?
- Demonstrates a **tiny but complete** repo layout (README, LICENSE, CI, lint, tests).
- Uses **modern Python tooling** (`uv` for dependency management & virtual‑env, `ruff` for lint/format, `pytest` for testing).
- Shows a **single‑command** build & test workflow (`make test`).
- Provides a **status badge** and graceful error handling.

## Install (one‑liner)
```sh
# Using uv – the recommended installer for tiny Python projects
uv tool install moodlog
```
Or, if you prefer pipx:
```sh
pipx install moodlog
```

## Usage
```sh
# Add an entry (you will be prompted for mood & optional note)
$ moodlog add
? Mood: happy
? Note (optional): finished the report
Entry added! 🎉

# List the last 5 entries
$ moodlog list --count 5
1️⃣ 2024‑05‑23 14:12 – happy – finished the report
2️⃣ 2024‑05‑22 09:03 – stressed – deadline looming
…

# Show simple statistics
$ moodlog stats
happy    ▓▓▓▓▓ (3)
stressed ▓ (1)
```

## Development
### Prerequisites
- **uv** – install from https://github.com/astral-sh/uv
- **git** – for cloning the repo

```sh
# Clone the repo
git clone https://github.com/your-handle/moodlog.git
cd moodlog

# Create a dev environment (uv does this automatically)
uv sync

# Run the CLI from source
uv run moodlog --help
```

### Testing & linting
```sh
make test        # runs pytest + coverage
make lint        # runs ruff in check mode
```

### CI
The repository uses **GitHub Actions** to run lint, tests, and type checking on every push/PR. The workflow lives in `.github/workflows/ci.yml`.

## License
MIT – see `LICENSE`.

## Security
If you discover a vulnerability, please email <topherbot@proton.me>.
