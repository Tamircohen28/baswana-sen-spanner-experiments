"""Experiment orchestration for spanner evaluation."""

from itertools import product
import math
import os
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from ..graphs.erdos_renyi import generate_erdos_renyi_graph
from ..spanners.baswana_sen import build_spanner_baswana_sen
from .stretch import compute_stretch_sampled_edges, compute_stretch_sampled_pairs
from .metrics import compute_theoretical_bound
from ..utils.timing import Timer


def timed(func: Callable) -> Tuple[Any, float]:
    """Helper to time a function call and return (result, elapsed_time)."""
    with Timer() as timer:
        result = func()
    return result, timer.elapsed


def run_single_experiment(n: int, p: float, k: int, rep: int, base_seed: int, n_stretch_samples: int) -> Dict:
    """Run a single experiment: generate graph, build spanner, compute metrics."""
    # Validate k: must be integer >= 2 and <= log(n)
    if not isinstance(k, int) or k < 2:
        raise ValueError(f"k must be an integer >= 2, got k={k}")
    if n > 1:
        max_k = int(math.log(n))
        if k > max_k:
            raise ValueError(f"k={k} is invalid for n={n}. k must be <= log({n}) = {max_k}")
    
    seed = base_seed + rep
    
    # Generate graph
    (G, n_original, n_connected), time_gen = timed(lambda: generate_erdos_renyi_graph(n, p, seed))
    n_edges_G = sum(len(neighbors) for neighbors in G.values()) // 2
    
    # Build spanner
    H, time_spanner = timed(lambda: build_spanner_baswana_sen(G, k, seed + 1000))
    n_edges_H = sum(len(neighbors) for neighbors in H.values()) // 2
    
    # Compute theoretical bound
    theoretical_bound = compute_theoretical_bound(n_connected, k)
    spanner_size_ratio = n_edges_H / theoretical_bound if theoretical_bound > 0 else 0.0
    
    # Compute stretch on sampled edges (for performance, always use sampling instead of exact computation)
    stretch_edges, time_stretch_edges = timed(lambda: compute_stretch_sampled_edges(G, H, n_stretch_samples, seed + 2000))
    
    # Compute stretch on sampled pairs
    stretch_pairs, time_stretch_pairs = timed(lambda: compute_stretch_sampled_pairs(G, H, n_stretch_samples, seed + 2000))
    
    return {
        'n': n, 'p': p, 'k': k, 'rep': rep, 'seed': seed,
        'n_original': n_original, 'n_connected': n_connected,
        'n_edges_G': n_edges_G, 'spanner_size': n_edges_H,
        'theoretical_bound': theoretical_bound, 'spanner_size_ratio': spanner_size_ratio,
        'max_stretch_edges': stretch_edges['max_stretch'],
        'avg_stretch_edges': stretch_edges['avg_stretch'],
        'max_stretch_pairs': stretch_pairs['max_stretch'],
        'avg_stretch_pairs': stretch_pairs['avg_stretch'],
        'time_gen': time_gen, 'time_spanner': time_spanner,
        'time_stretch': time_stretch_edges + time_stretch_pairs,
        'n_infinite_stretch_edges': stretch_edges.get('n_infinite', 0),
        'n_infinite_stretch_pairs': stretch_pairs.get('n_infinite', 0),
    }


def run_experiment_suite(n_values: List[int], p_values: List[float], k_values: List[int], n_reps: int, base_seed: int, n_stretch_samples: int, output_path: Optional[str] = None) -> pd.DataFrame:
    """Run a full suite of experiments over all parameter combinations. Saves results incrementally if output_path is provided."""
    # Validate n values: all must be > 100
    for n in n_values:
        if n <= 100:
            raise ValueError(f"All n values must be > 100, got n={n}")
    
    # Validate k values: must be integers >= 2 and <= log(n) for all n values
    for k in k_values:
        if not isinstance(k, int) or k < 2:
            raise ValueError(f"k values must be integers >= 2, got k={k}")
    for n in n_values:
        max_k = int(math.log(n))
        invalid_ks = [k for k in k_values if k > max_k]
        if invalid_ks:
            raise ValueError(f"k values {invalid_ks} are invalid for n={n}. k must be <= log({n}) = {max_k}")
    
    results = []
    total_experiments = len(n_values) * len(p_values) * len(k_values) * n_reps
    experiments_per_n = len(p_values) * len(k_values) * n_reps
    
    # Track average runtime per n value
    n_avg_times = {}  # n -> (total_time, count)
    prev_n = None
    prev_avg_time = None
    
    # Initialize output file if path provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if not os.path.exists(output_path):
            df_header = pd.DataFrame(columns=[
                'n', 'p', 'k', 'rep', 'seed', 'n_original', 'n_connected',
                'n_edges_G', 'spanner_size', 'theoretical_bound', 'spanner_size_ratio',
                'max_stretch_edges', 'avg_stretch_edges', 'max_stretch_pairs', 'avg_stretch_pairs',
                'time_gen', 'time_spanner', 'time_stretch',
                'n_infinite_stretch_edges', 'n_infinite_stretch_pairs'
            ])
            df_header.to_csv(output_path, index=False)
    
    with tqdm(total=total_experiments, desc="Running experiments") as pbar:
        current_n = None
        experiments_in_current_n = 0
        
        for n, p, k, rep in product(n_values, p_values, k_values, range(n_reps)):
            # Detect when we move to a new n value
            if n != current_n:
                current_n = n
                experiments_in_current_n = 0
                # Initialize with estimate from previous n if available
                if prev_n is not None and prev_avg_time is not None:
                    # O(n^2) scaling: time scales as (n2/n1)^2
                    ratio = n / prev_n
                    estimated_avg_time = (prev_avg_time * ratio) ** 2
                    n_avg_times[n] = (estimated_avg_time, 1)  # Initialize with estimate
                else:
                    n_avg_times[n] = (0.0, 0)  # Will be updated after first experiment
            
            start_time = time.time()
            
            try:
                result = run_single_experiment(n, p, k, rep, base_seed, n_stretch_samples)
                results.append(result)
                
                # Save result immediately if output path provided
                if output_path:
                    df_row = pd.DataFrame([result])
                    df_row.to_csv(output_path, mode='a', header=False, index=False)
            except Exception as e:
                print(f"\nError in experiment n={n}, p={p}, k={k}, rep={rep}: {e}")
                error_result = {'n': n, 'p': p, 'k': k, 'rep': rep, 'seed': base_seed + rep, 'error': str(e)}
                results.append(error_result)
                if output_path:
                    df_row = pd.DataFrame([error_result])
                    df_row.to_csv(output_path, mode='a', header=False, index=False)
            
            elapsed = time.time() - start_time
            experiments_in_current_n += 1
            
            # Update average time for current n
            total_time, count = n_avg_times[n]
            n_avg_times[n] = (total_time + elapsed, count + 1)
            current_avg_time = n_avg_times[n][0] / n_avg_times[n][1]
            
            # Time remaining for current n
            remaining_in_current_n = experiments_per_n - experiments_in_current_n
            remaining_time = current_avg_time * remaining_in_current_n
            
            # Time for remaining n values (using O(n^2) scaling)
            # Chain estimates: each next n's estimate is based on the previous n's estimate
            current_n_idx = n_values.index(n)
            remaining_n_values = n_values[current_n_idx + 1:]
            
            if remaining_n_values:
                # Start with current n's avg time as base for chaining
                prev_estimated_avg_time = current_avg_time
                prev_n_for_estimate = n
                
                for next_n in remaining_n_values:
                    # Calculate ratio between consecutive n values
                    ratio = next_n / prev_n_for_estimate
                    
                    # Update estimate based on previous estimate (chaining)
                    # For O(n^2) scaling: time scales as (n2/n1)^2, so multiply by ratio^2
                    # Correct formula: prev_time * (ratio^2), not (prev_time * ratio)^2
                    estimated_avg_time_next = prev_estimated_avg_time * (ratio ** 2)
                    remaining_time += estimated_avg_time_next * experiments_per_n
                    
                    # Update for next iteration
                    prev_estimated_avg_time = estimated_avg_time_next
                    prev_n_for_estimate = next_n
            
            # Update progress bar with remaining time
            if remaining_time > 0:
                pbar.set_postfix({'est_remaining': f'{remaining_time:.0f}s'})
            
            pbar.update(1)
            
            # Update previous n info for next iteration
            if experiments_in_current_n == experiments_per_n:
                prev_n = n
                prev_avg_time = current_avg_time
    
    return pd.DataFrame(results)
