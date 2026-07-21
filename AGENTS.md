# Baswana-Sen Spanner Experiments — AGENTS.md

## Overview

Experimental evaluation of the **Baswana–Sen randomized algorithm** for constructing **(2k-1)-spanners** on Erdős–Rényi random graphs, with a Greedy Spanner baseline comparison.

## Commands

| Command | Purpose |
|---------|---------|
| `make install` | Create venv and install Python dependencies |
| `make test` | Run setup verification and smoke tests |
| `make lint` | Byte-compile Python sources |
| `make agent:check` | Drift + feature equivalence + platform targets |
| `python scripts/run_all_experiments.py` | Full experiment suite |
| `python scripts/run_comparison.py` | Baswana-Sen vs Greedy comparison |

## Project layout

- `src/graphs/` — Erdős–Rényi graph generation
- `src/spanners/` — Baswana-Sen and Greedy spanner algorithms
- `src/evaluation/` — Metrics, stretch, experiment orchestration
- `notebooks/` — Analysis and visualization (Colab-friendly)
- `data/processed/` — Timestamped CSV experiment results

## Constraints

- Never commit secrets, credentials, or large generated datasets beyond checked-in samples
- Use deterministic seeds (`src/utils/seeding.py`) for reproducible experiments
- CI uses `ubuntu-latest` only
- Prefer `make install` / `make test` over ad-hoc pip commands in docs

## Algorithm notes

- Graphs use adjacency lists; stretch via BFS on unweighted graphs
- Disconnected graphs: largest connected component is extracted before spanner construction
- Baswana-Sen requires `k >= 2` and `k <= log(n)` per graph size

## Versioning

See [docs/engineering/build-and-release/versioning.md](docs/engineering/build-and-release/versioning.md).
Update `docs/CHANGELOG.md` and root `CHANGELOG.md` under `[Unreleased]` before each release.

## Dependency management

- Dependabot manages `requirements.txt` (weekly) and GitHub Actions (monthly)
- Do not blindly merge Dependabot PRs — require CI green first
