# Architecture overview

## Modules

```
src/
├── graphs/erdos_renyi.py      # G(n,p) generation + largest component extraction
├── spanners/
│   ├── baswana_sen.py         # Randomized (2k-1)-spanner
│   └── greedy.py              # Deterministic greedy baseline
├── evaluation/
│   ├── experiments.py         # Batch experiment runner
│   ├── stretch.py             # BFS stretch metrics
│   └── metrics.py             # Aggregation helpers
└── utils/                     # Seeding and timing
```

## Data flow

1. Generate Erdős–Rényi graph (optionally extract largest component)
2. Construct spanner (Baswana-Sen or Greedy)
3. Sample stretch on edges and vertex pairs
4. Append row to CSV in `data/processed/`

## Notebooks

Notebooks load CSV results and produce figures for the academic report in `docs/Report.tex`.
