# Experimental Evaluation of the Baswana-Sen Spanner Algorithm

**Author:** Tamir Cohen  
**Email:** tamirnoy@post.bgu.ac.il

This work is part of the Mini-Project on Low-Distortion Embeddings (BGU).

---

## Overview

This project presents an experimental evaluation of the **Baswana-Sen randomized algorithm** for constructing **(2k-1)-spanners** on Erdős–Rényi random graphs. A spanner is a sparse subgraph that preserves approximate distances, and the Baswana-Sen algorithm is a well-known randomized approach that achieves a good trade-off between sparsity and stretch.

### What is a Spanner?

Given a graph G, a (2k-1)-spanner H is a subgraph of G such that for any two vertices u and v, the distance in H is at most (2k-1) times the distance in G. The parameter k controls the trade-off: larger k values produce sparser spanners (fewer edges) but with higher stretch (distance distortion).

### Why This Experiment?

The Baswana-Sen algorithm has a theoretical guarantee: it produces a spanner with O(k·n^(1+1/k)) edges in expectation. However, theoretical bounds don't always reflect practical performance. This experiment aims to:

1. **Verify theoretical bounds empirically**: How close is the actual spanner size to the theoretical bound O(k·n^(1+1/k))?
2. **Measure stretch in practice**: Does the algorithm achieve the promised (2k-1) stretch bound, and what is the average stretch?
3. **Understand parameter sensitivity**: How do different values of k, graph size (n), and edge density (p) affect spanner quality and construction time?

---

## The Experiment

### Experimental Design

We evaluated the Baswana-Sen algorithm on Erdős–Rényi random graphs G(n,p), where:
- **n** is the number of vertices (graph size)
- **p** is the edge probability (controls graph density)
- **k** is the spanner parameter (controls the stretch-sparsity trade-off)

### Parameters Tested

- **Graph sizes (n)**: 500, 1000, 2000 vertices
- **Edge probabilities (p)**: We tested multiple densities (computed per n value):
  - Sparse: log(n)/n (near connectivity threshold)
  - Medium: n^(-1/2)
  - Dense: 0.1, 0.2, 0.3
  - This results in 9 unique p values across all n values
- **Spanner parameters (k)**: 2, 3, 4, 5
  - Note: k must be an integer >= 2 and <= log(n) for each n value
- **Repetitions**: 5 runs per configuration for statistical reliability
- **Stretch samples**: 1000 sampled edges and 1000 sampled vertex pairs per experiment

### What We Measured

For each experiment, we recorded:

1. **Spanner size**: Number of edges in the constructed spanner H
2. **Size ratio**: Actual size divided by theoretical bound O(k·n^(1+1/k))
3. **Stretch**: 
   - Maximum stretch over sampled edges and vertex pairs
   - Average stretch over sampled edges and vertex pairs
4. **Running time**: Time to generate graph, construct spanner, and compute stretch

### Why These Choices?

- **Erdős–Rényi graphs**: Simple, well-understood random graph model that allows systematic exploration of different graph densities
- **Multiple k values**: To understand how the stretch-sparsity trade-off behaves in practice
- **Sampling for stretch**: Computing exact stretch for all pairs is computationally expensive (O(n²) pairs), so we sample edges and vertex pairs to estimate stretch efficiently
- **Largest connected component**: For disconnected graphs, we focus on the largest connected component to ensure meaningful distance measurements

---

## Results

The experimental results are stored in timestamped CSV files in `data/processed/` (e.g., `experiments-results-DD-MM-YYYY-HH-MM-SS.csv`) and can be analyzed using the provided Jupyter notebooks. The most recent results file contains 540 experiments (3 n values × 9 p values × 4 k values × 5 repetitions).

Key findings include:

- **Spanner size**: Empirical spanner sizes compared to the theoretical bound O(k·n^(1+1/k))
- **Stretch bounds**: Verification that the (2k-1) stretch bound is satisfied
- **Parameter sensitivity**: How spanner quality and construction time vary with n, p, and k

Detailed analysis and visualizations are available in the notebooks (see below).

---

## How to Reproduce

### Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Verify setup:
   ```bash
   python verify_setup.py
   ```

### Running Experiments

Run the full experiment suite:
```bash
python scripts/run_all_experiments.py
```

This will generate results in `data/processed/experiments-results-DD-MM-YYYY-HH-MM-SS.csv` (timestamped filename). The script supports various parameters (see `--help` for details). The default configuration runs:
- n values: [500, 1000, 2000]
- p values: log(n)/n, n^(-1/2), 0.1, 0.2, 0.3 (computed per n value)
- k values: [2, 3, 4, 5] (automatically adjusted to be valid for all n values)
- repetitions: 5
- stretch samples: 1000

### Analyzing Results

Three Jupyter notebooks are provided:

1. **`01_baswana_sen_sanity_check.ipynb`**: Verification that the algorithm works correctly on small examples
2. **`02_experiments_main.ipynb`**: Load and analyze experiment results, compute summary statistics
3. **`03_plots_and_results.ipynb`**: Generate publication-ready figures and tables

Start Jupyter:
```bash
jupyter lab
# or
jupyter notebook
```

---

## Implementation Notes

### Design Decisions

- **Graph representation**: Custom adjacency lists for efficiency with large graphs
- **Unweighted graphs**: Focus on unweighted graphs using BFS for distance computation
- **Deterministic seeding**: All random operations use deterministic seeds for reproducibility
- **Sampling for stretch**: For performance, we sample 1000 edges and 1000 vertex pairs per experiment rather than computing exact stretch for all pairs
- **k parameter constraints**: The algorithm requires k >= 2 and k <= log(n) for each graph size n
- **Incremental saving**: Results are saved incrementally to CSV files during execution to prevent data loss

### Reproducibility

All experiments use deterministic random seeds. To reproduce exact results:
- Use the same Python version (3.8+)
- Install exact dependencies from `requirements.txt`
- Use the same base seed (default: 42)

---

## Project Structure

```
baswana-sen-spanner-experiments/
├── src/                    # Implementation code
│   ├── graphs/            # Graph generation (Erdős–Rényi)
│   ├── spanners/          # Baswana-Sen algorithm
│   ├── evaluation/        # Experiment orchestration and metrics
│   └── utils/            # Utilities (seeding, timing)
├── notebooks/            # Analysis notebooks
├── scripts/              # Experiment runner
├── data/processed/       # Experiment results (CSV)
└── requirements.txt      # Python dependencies
```

---

## Dependencies

- numpy>=1.24.0: Numerical computations
- scipy>=1.10.0: Scientific computing
- pandas>=2.0.0: Data analysis
- matplotlib>=3.7.0: Plotting
- seaborn>=0.12.0: Statistical visualizations
- jupyter>=1.0.0, jupyterlab>=4.0.0: Interactive notebooks
- networkx>=3.0: Graph utilities (for visualization only)
- tqdm>=4.65.0: Progress bars

See `requirements.txt` for exact versions.

---

## License

See `LICENSE` file for details.
