# app

Onboarding sandbox. Python project managed with [uv](https://docs.astral.sh/uv/).

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
uv sync
```

This creates `.venv/` and installs runtime + dev dependencies.

## Run

```bash
uv run python -m app.main
```

## Test

```bash
uv run pytest
```

## Lint & format

```bash
uv run ruff check .          # lint
uv run ruff check --fix .    # autofix
uv run ruff format .         # format
```

## Pre-commit hooks (recommended)

```bash
uv run pre-commit install
```

After install, `ruff` + whitespace fixers run on every `git commit`.

## Layout

```
src/app/        # application code
tests/          # pytest tests
pyproject.toml  # project + tool config
AGENTS.md       # conventions for humans and agents
```

## Ship a change

1. Branch: `git checkout -b feat/<short-name>`
2. Make the change, add/adjust a test in `tests/`.
3. `uv run pytest` — green.
4. Commit (pre-commit will lint/format).
5. Push and open a PR; one review approval merges.

See [AGENTS.md](./AGENTS.md) for full conventions.
