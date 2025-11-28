"""Experiment orchestration for spanner evaluation."""

import os
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

from ..graphs.erdos_renyi import generate_erdos_renyi_graph
from ..spanners.baswana_sen import build_spanner_baswana_sen
from .stretch import compute_stretch_edges, compute_stretch_sampled_pairs
from .metrics import compute_theoretical_bound
from ..utils.timing import Timer
from ..utils.seeding import set_seed


def run_single_experiment(
    n: int, 
    p: float, 
    k: int, 
    rep: int, 
    base_seed: int = 42,
    n_stretch_samples: int = 10000
) -> Dict:
    """
    Run a single experiment: generate graph, build spanner, compute metrics.
    
    Args:
        n: Number of vertices
        p: Edge probability
        k: Spanner parameter
        rep: Repetition number
        base_seed: Base seed for random number generation
        n_stretch_samples: Number of pairs to sample for stretch computation
        
    Returns:
        Dictionary with experiment results
    """
    seed = base_seed + rep
    
    # Generate graph
    with Timer() as timer:
        G, n_original, n_connected = generate_erdos_renyi_graph(n, p, seed)
    time_gen = timer.elapsed
    
    # Count edges in G
    n_edges_G = sum(len(neighbors) for neighbors in G.values()) // 2
    
    # Build spanner
    with Timer() as timer:
        H = build_spanner_baswana_sen(G, k, seed + 1000)  # Different seed for spanner
    time_spanner = timer.elapsed
    
    # Count edges in H
    n_edges_H = sum(len(neighbors) for neighbors in H.values()) // 2
    
    # Compute theoretical bound
    theoretical_bound = compute_theoretical_bound(n_connected, k)
    spanner_size_ratio = n_edges_H / theoretical_bound if theoretical_bound > 0 else 0.0
    
    # Compute stretch on edges
    with Timer() as timer:
        stretch_edges = compute_stretch_edges(G, H)
    time_stretch_edges = timer.elapsed
    
    # Compute stretch on sampled pairs
    with Timer() as timer:
        stretch_pairs = compute_stretch_sampled_pairs(G, H, n_stretch_samples, seed + 2000)
    time_stretch_pairs = timer.elapsed
    
    time_stretch = time_stretch_edges + time_stretch_pairs
    
    # Prepare result row
    result = {
        'n': n,
        'p': p,
        'k': k,
        'rep': rep,
        'seed': seed,
        'n_original': n_original,
        'n_connected': n_connected,
        'n_edges_G': n_edges_G,
        'spanner_size': n_edges_H,
        'theoretical_bound': theoretical_bound,
        'spanner_size_ratio': spanner_size_ratio,
        'max_stretch_edges': stretch_edges['max_stretch'],
        'avg_stretch_edges': stretch_edges['avg_stretch'],
        'max_stretch_pairs': stretch_pairs['max_stretch'],
        'avg_stretch_pairs': stretch_pairs['avg_stretch'],
        'time_gen': time_gen,
        'time_spanner': time_spanner,
        'time_stretch': time_stretch,
        'n_infinite_stretch_edges': stretch_edges.get('n_infinite', 0),
        'n_infinite_stretch_pairs': stretch_pairs.get('n_infinite', 0),
    }
    
    return result


def run_experiment_suite(
    n_values: List[int],
    p_values: List[float],
    k_values: List[int],
    n_reps: int,
    base_seed: int = 42,
    n_stretch_samples: int = 10000
) -> pd.DataFrame:
    """
    Run a full suite of experiments over all parameter combinations.
    
    Args:
        n_values: List of vertex counts
        p_values: List of edge probabilities
        k_values: List of spanner parameters
        n_reps: Number of repetitions per combination
        base_seed: Base seed for random number generation
        n_stretch_samples: Number of pairs to sample for stretch computation
        
    Returns:
        DataFrame with all experiment results
    """
    results = []
    
    # Compute total number of experiments
    total_experiments = len(n_values) * len(p_values) * len(k_values) * n_reps
    
    # Create progress bar
    with tqdm(total=total_experiments, desc="Running experiments") as pbar:
        for n in n_values:
            for p in p_values:
                for k in k_values:
                    for rep in range(n_reps):
                        try:
                            result = run_single_experiment(
                                n, p, k, rep, base_seed, n_stretch_samples
                            )
                            results.append(result)
                        except Exception as e:
                            # Log error but continue
                            print(f"\nError in experiment n={n}, p={p}, k={k}, rep={rep}: {e}")
                            result = {
                                'n': n,
                                'p': p,
                                'k': k,
                                'rep': rep,
                                'seed': base_seed + rep,
                                'error': str(e)
                            }
                            results.append(result)
                        pbar.update(1)
    
    df = pd.DataFrame(results)
    return df


def save_results(df: pd.DataFrame, path: str) -> None:
    """
    Save experiment results to CSV file.
    
    Creates parent directories if they don't exist.
    
    Args:
        df: DataFrame with results
        path: Output file path
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Results saved to {path}")

