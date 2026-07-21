# Concepts

## Spanners

A **(2k-1)-spanner** H of graph G is a sparse subgraph where every pair distance in H is at most (2k−1) times the distance in G. Larger k → sparser H, higher stretch bound.

## Baswana-Sen algorithm

Randomized multi-phase clustering algorithm with expected O(k·m) time and O(k·n^(1+1/k)) edges.

## Greedy baseline

Deterministic spanner from Althöfer et al. (1993). Accurate but O(m·n) — used only on smaller graphs in this repo.

## Parameters

| Symbol | Meaning |
|--------|---------|
| n | Number of vertices |
| p | Erdős–Rényi edge probability |
| k | Spanner parameter (integer ≥ 2, ≤ log n) |

## Metrics

- **Spanner size** — edge count in H
- **Stretch** — sampled max/average distortion vs G
- **Size ratio** — empirical size / theoretical bound
