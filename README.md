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

## Deploy

Live URL: **https://hockinghills.github.io/emp-app/** — reload and check
that the short SHA matches `git rev-parse HEAD` to confirm the latest
push is live.

The smallest deployable artifact is a static page that prints the live
commit SHA and build time. It is built by `scripts/build_site.py` into
`_site/index.html`.

### Local

```bash
uv run python scripts/build_site.py
python -m http.server -d _site 8000   # then open http://localhost:8000
```

### Production (push-to-main)

On every push to `main`, GitHub Actions:

1. Runs lint + tests (`.github/workflows/ci.yml`).
2. Builds the site and deploys it to GitHub Pages
   (`.github/workflows/deploy.yml`).

The deployed page shows the `GITHUB_SHA` it was built from, so the path
from "I made an edit" to "it is live" is verifiable by reloading the
Pages URL and confirming the short SHA matches `git rev-parse HEAD`.

### Current status

Remote: `git@github.com:hockinghills/emp-app.git`. Pages source is
**GitHub Actions** — every push to `main` runs `deploy.yml` and
publishes the built artifact via `actions/deploy-pages`.

### Health checks

The CLI ships `--version` and `--health` flags so a deployed build can
be probed without browsing the site:

```bash
uv run python -m app.main --version   # -> 0.0.1
uv run python -m app.main --health    # -> ok
```
