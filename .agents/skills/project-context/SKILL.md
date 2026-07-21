---
name: project-context
description: 'Project context for Baswana-Sen spanner experiments — algorithm goals, structure, parameters, and workflow. Use when implementing or modifying spanner code, running experiments, or analyzing results.'
---

# Baswana-Sen Spanner Experiments

## Goals

1. Implement Baswana-Sen and Greedy spanner algorithms correctly
2. Evaluate on Erdős–Rényi G(n,p) graphs across n, p, k
3. Measure spanner size, stretch, and runtime
4. Produce reproducible CSV results and notebook visualizations

## Key decisions

- Custom adjacency lists (not NetworkX) for performance
- Unweighted graphs; BFS for distances
- Largest connected component when G is disconnected
- Deterministic seeds via `set_seed()`

## Default experiment parameters

See `scripts/run_all_experiments.py` — typical n ∈ {500,1000,2000}, k ∈ {2,3,4,5}, 5 repetitions.

## Commands

```bash
make install && make test
python scripts/run_all_experiments.py
jupyter lab
```

Policy and constraints: root [AGENTS.md](../../../AGENTS.md).
