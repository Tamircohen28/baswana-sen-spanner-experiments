# Quick start

## Prerequisites

- Python 3.8 or higher (3.12 recommended)
- `make` (optional but preferred)

## Install

```bash
make install
make test
```

### Alternative (manual)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python verify_setup.py
```

## Run experiments

```bash
source .venv/bin/activate
python scripts/run_all_experiments.py
```

Compare against the Greedy baseline:

```bash
python scripts/run_comparison.py
```

## Notebooks

```bash
jupyter lab
```

Open notebooks in `notebooks/` — Colab links are in the root README.

## AI assistants

| Platform | Entry point |
|----------|-------------|
| Claude Code | `CLAUDE.md` → `AGENTS.md` |
| Cursor | `.cursor/rules/000-project.mdc` |
| Codex | Root `AGENTS.md` |
