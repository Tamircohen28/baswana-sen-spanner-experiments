# Baswana-Sen Spanner Experiments - Project Context

## Project Objectives

This repository implements and experimentally evaluates the **Baswana–Sen randomized algorithm** for constructing **(2k-1)-spanners** on Erdős–Rényi random graphs.

### Primary Goals

1. **Implement the Baswana-Sen algorithm** correctly and efficiently
2. **Generate random graphs** (Erdős–Rényi G(n,p)) for various n and p
3. **Construct (2k-1)-spanners** for several values of k
4. **Measure key metrics**:
   - Spanner size vs. theoretical bound O(k n^(1+1/k))
   - Stretch (max, average, sampled pairs)
   - Running time (empirical complexity)
5. **Produce clean, reproducible experiments and plots** for academic reporting

## Key Implementation Decisions

### Graph Representation
- **Decision**: Custom adjacency list (`dict[int, list[int]]`) for efficiency
- **Rationale**: Better performance for large graphs, avoids NetworkX overhead
- **Note**: NetworkX is used only for visualization in notebooks

### Graph Type
- **Decision**: Start with **unweighted graphs** (BFS-based stretch computation)
- **Rationale**: Simpler implementation, matches initial requirements
- **Future**: Can extend to weighted graphs later if needed

### Connectivity Handling
- **Decision**: Use **largest connected component** for disconnected graphs
- **Rationale**: Ensures valid spanner construction, maintains graph properties
- **Implementation**: BFS-based component extraction with vertex relabeling

### Random Seeding
- **Decision**: Deterministic seeding for reproducibility
- **Implementation**: `set_seed()` function sets both `random` and `numpy.random`
- **Usage**: Base seed + repetition index for experiment reproducibility

## Project Structure

```
baswana-sen-spanner-experiments/
├── src/                    # Source code modules
│   ├── graphs/            # Graph generation
│   │   └── erdos_renyi.py
│   ├── spanners/          # Spanner algorithms
│   │   └── baswana_sen.py
│   ├── evaluation/       # Evaluation and experiments
│   │   ├── stretch.py
│   │   ├── experiments.py
│   │   └── metrics.py
│   └── utils/            # Utilities
│       ├── seeding.py
│       └── timing.py
├── notebooks/            # Jupyter notebooks
│   ├── 01_baswana_sen_sanity_check.ipynb
│   ├── 02_experiments_main.ipynb
│   └── 03_plots_and_results.ipynb
├── scripts/              # CLI scripts
│   └── run_all_experiments.py
├── data/                 # Data storage
│   ├── raw/             # Raw graph data (optional)
│   └── processed/       # Experiment results (CSV)
└── results/             # Output files
    ├── figures/         # Plots (PNG/PDF)
    └── tables/          # Summary tables
```

## Algorithm Details

### Baswana-Sen Algorithm
- **Input**: Graph G, parameter k, random seed
- **Output**: (2k-1)-spanner H
- **Complexity**: Expected O(k * m) where m = |E(G)|
- **Phases**:
  1. Phase 0: Initialize all vertices in their own clusters
  2. Phases 1 to k-1: Sample clusters, form new clusters, add edges
  3. Phase k: Add edges for remaining vertices

### Stretch Computation
- **Edge stretch**: For each edge (u,v) in G, compute d_H(u,v) / d_G(u,v)
- **Sampled pairs**: Sample random vertex pairs, compute stretch
- **Metrics**: Max stretch, average stretch, distribution

## Experiment Parameters

### Default Configuration
- **n values**: [5000, 10000, 20000, 50000]
- **p values**: [log(n)/n, n^(-1/2), 0.1, 0.2, 0.3] (computed per n)
- **k values**: [1, 2, 3, 4, 5]
- **Repetitions**: 10 per combination
- **Base seed**: 42

### Running Experiments
```bash
# Activate virtual environment
source venv/bin/activate

# Run with default parameters
python scripts/run_all_experiments.py

# Custom parameters
python scripts/run_all_experiments.py --max-n 20000 --reps 5 --k-values 1 2 3
```

## Dependencies

### Core Libraries
- **numpy**: Numerical computations
- **scipy**: Scientific computing (optional, for future extensions)
- **networkx**: Graph utilities (for visualization only)
- **pandas**: Data analysis and CSV handling
- **matplotlib**: Plotting
- **jupyter/jupyterlab**: Interactive notebooks
- **tqdm**: Progress bars

### Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Output Files

### Data Files
- `data/processed/experiments_full.csv`: Complete experiment results

### Figures (from notebook 03)
- `results/figures/spanner_size_vs_k.png/pdf`
- `results/figures/stretch_vs_k.png/pdf`
- `results/figures/runtime_vs_n.png/pdf`
- `results/figures/spanner_size_ratio.png/pdf`

## Notebook Workflow

1. **01_baswana_sen_sanity_check.ipynb**: 
   - Small graph tests
   - Visualization
   - Stretch verification

2. **02_experiments_main.ipynb**:
   - Load experiment results
   - Summary statistics
   - Aggregation by parameters

3. **03_plots_and_results.ipynb**:
   - Generate all plots
   - Save figures for report
   - Create summary tables

## Performance Considerations

- Use efficient BFS (queue-based, not recursive)
- Minimize graph format conversions
- Cache distance computations where possible
- Use numpy for random sampling
- Progress tracking with tqdm for long experiments

## Reproducibility

- All stochastic operations use deterministic seeds
- Experiment runner records: n, p, k, repetition index, random seed
- Results stored in CSV for downstream analysis
- Virtual environment ensures consistent dependencies

## Testing and Validation

- Sanity checks in algorithm: verify H is subgraph of G, connectivity preserved
- Stretch bound verification on small graphs
- Test cases included in notebooks

## Future Extensions

- Weighted graph support
- Additional spanner algorithms for comparison
- Parallel experiment execution
- More sophisticated visualization

## Notes

- Graph generation uses largest connected component
- Vertices are relabeled 0..(n_cc-1) after component extraction
- Spanner construction uses separate seed from graph generation for independence
- Stretch computation handles unreachable cases (returns inf or excludes)

