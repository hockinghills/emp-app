# AGENTS.md

Conventions for humans and agents working in this repo. Read this before your first commit.

## Stack

- **Language:** Python 3.11+
- **Package manager:** [uv](https://docs.astral.sh/uv/)
- **Lint + format:** [ruff](https://docs.astral.sh/ruff/) (one tool, both jobs)
- **Tests:** pytest
- **Pre-commit:** [pre-commit](https://pre-commit.com/) running ruff + basic hygiene hooks

Choices are deliberately boring. Reverse them when the work demands it; don't reverse them for taste.

## Layout

```
src/app/        # application code (importable as `app`)
tests/          # pytest tests, mirror src/ structure where useful
pyproject.toml  # single source of truth for deps + tool config
```

`src/` layout means tests import the installed package, not a sibling directory — this catches packaging bugs early.

## Setup

```bash
uv sync                       # install runtime + dev deps into .venv/
uv run pre-commit install     # optional but recommended
```

## Run / test / lint

```bash
uv run python -m app.main     # run
uv run pytest                 # tests
uv run ruff check .           # lint
uv run ruff format .          # format
```

All commands work without activating a venv — `uv run` handles it.

## Branch naming

`<type>/<short-kebab-name>` where `<type>` is one of:

- `feat/` — new feature
- `fix/` — bug fix
- `chore/` — tooling, deps, refactors with no behavior change
- `docs/` — docs only

Example: `feat/login-rate-limit`, `fix/null-deref-on-empty-input`.

## Commit style

- Imperative present tense: "add X", not "added X" or "adds X".
- Keep the subject ≤ 72 chars. Body wrapped at ~100 if needed.
- Reference issues by id where applicable (e.g. `EMP-3`).
- One logical change per commit when practical.

Example:

```
Add greet() helper and smoke test

Lays the foundation for future onboarding sandbox features. No
behavior outside the new module.

EMP-2
```

Agents committing on behalf of Paperclip must include:

```
Co-Authored-By: Paperclip <noreply@paperclip.ing>
```

## Tests

- Tests live in `tests/`.
- Default to `pytest`-style: top-level `def test_*` functions, plain `assert`.
- Add at least one test for every new function or bug fix. The bar is "demonstrates intent", not "100% coverage".
- Tests must pass before merge (`uv run pytest`).

## Lint / format

- `ruff check` is required to pass. Use `--fix` for auto-fixable issues.
- `ruff format` is the only formatter. Do not hand-format.
- Pre-commit runs both on staged files; CI (when added) will run them across the repo.

## Shipping a change (PR flow)

1. Branch from `main`.
2. Make the change. Add/adjust tests.
3. `uv run pytest` green locally.
4. `git commit` — pre-commit will lint/format. Fix and re-stage if it modifies files.
5. Push and open a PR. One reviewer approval merges into `main`.

`main` is always green. If `main` is red, dropping everything to fix it is the highest-priority work in the repo.

## Adding a dependency

```bash
uv add <package>              # runtime dep
uv add --dev <package>        # dev-only dep
```

`uv` updates `pyproject.toml` and `uv.lock`. Commit both.

## Out of scope (for now)

- CI: tracked separately. Until CI exists, local `uv run pytest` is the gate.
- Deploy pipeline: tracked separately.

## Escalation

If something in this doc is wrong or in your way, fix it in the same PR as the work it's blocking. Conventions serve the work, not the other way around.
