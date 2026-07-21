# Development workflow

## Setup

```bash
make install
make test
```

## Branching

- Default branch: `main`
- Feature branches: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`
- Open PRs against `main`; CI must pass before merge

## Running experiments locally

```bash
source .venv/bin/activate
python scripts/run_all_experiments.py --help
```

Results land in `data/processed/` with timestamped filenames.

## Pre-PR checks

```bash
make test
make agent:check
```

Agents run `make repo-standards-gate` during repo-standards polish.
