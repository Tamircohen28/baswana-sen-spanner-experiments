#!/usr/bin/env python3
"""
Script to compare Baswana-Sen against the Greedy Spanner baseline.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.erdos_renyi import generate_erdos_renyi_graph
from src.spanners.baswana_sen import build_spanner_baswana_sen
from src.spanners.greedy import build_greedy_spanner
from src.evaluation.stretch import compute_stretch_sampled_pairs
from src.evaluation.metrics import compute_theoretical_bound
from src.utils.timing import Timer


def run_comparison(n_values=[500, 1000], p_values=[0.05], k_values=[2, 3], reps=3):
    results = []
    
    total_ops = len(n_values) * len(p_values) * len(k_values) * reps
    pbar = tqdm(total=total_ops, desc="Comparison Experiments")
    
    for n in n_values:
        for p in p_values:
            for rep in range(reps):
                # 1. Generate Graph
                seed = 42 + rep
                G, n_orig, n_conn = generate_erdos_renyi_graph(n, p, seed)
                m_G = sum(len(adj) for adj in G.values()) // 2
                
                for k in k_values:
                    # 2. Run Baswana-Sen
                    with Timer() as timer_bs:
                        bs_spanner = build_spanner_baswana_sen(G, k, seed+100)
                    t_bs = timer_bs.elapsed
                    m_bs = sum(len(adj) for adj in bs_spanner.values()) // 2
                    
                    # 3. Run Greedy
                    # Note: Greedy is slow, be careful with large N
                    with Timer() as timer_greedy:
                        greedy_spanner = build_greedy_spanner(G, k)
                    t_greedy = timer_greedy.elapsed
                    m_greedy = sum(len(adj) for adj in greedy_spanner.values()) // 2
                    
                    # 4. Compute basic metrics
                    theory_bound = compute_theoretical_bound(n_conn, k)
                    
                    # Stretch estimation (smaller sample for speed)
                    bs_stretch = compute_stretch_sampled_pairs(G, bs_spanner, n_samples=500, seed=seed)
                    gr_stretch = compute_stretch_sampled_pairs(G, greedy_spanner, n_samples=500, seed=seed)
                    
                    results.append({
                        'n': n_conn, 'p': p, 'k': k, 'rep': rep,
                        'edges_original': m_G,
                        'edges_bs': m_bs,
                        'edges_greedy': m_greedy,
                        'ratio_bs_theory': m_bs / theory_bound,
                        'ratio_greedy_theory': m_greedy / theory_bound,
                        'time_bs': t_bs,
                        'time_greedy': t_greedy,
                        'avg_stretch_bs': bs_stretch['avg_stretch'],
                        'avg_stretch_greedy': gr_stretch['avg_stretch']
                    })
                    pbar.update(1)
                    
    pbar.close()
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("Running baseline comparison...")
    # Restricted parameters to ensure it finishes in reasonable time
    df = run_comparison(n_values=[200, 500], p_values=[0.1], k_values=[2, 3], reps=2)
    
    print("\nResults Summary:")
    print(df.groupby(['n', 'k'])[['edges_bs', 'edges_greedy', 'time_bs', 'time_greedy']].mean())
    
    output_path = 'data/processed/comparison_results.csv'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

