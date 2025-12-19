#!/usr/bin/env python3
"""Command-line script to run all spanner experiments."""

import argparse
import math
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.experiments import run_experiment_suite


def main():
    """Main entry point for experiment runner."""
    parser = argparse.ArgumentParser(
        description='Run Baswana-Sen spanner experiments'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output CSV path. If not specified, generates timestamped filename: experiments-results-DD-MM-YYYY-HH-MM-SS.csv'
    )
    parser.add_argument(
        '--reps',
        type=int,
        default=5,
        help='Number of repetitions per parameter combination (default: 5)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Base random seed for reproducibility (default: 42)'
    )
    parser.add_argument(
        '--n-values',
        type=int,
        nargs='+',
        default=[500, 1000, 2000],
        help='Number of vertices in the graph (n). The Baswana-Sen algorithm constructs a (2k-1)-spanner on graphs with n vertices. All n values must be > 100. Default: [500, 1000, 2000]'
    )
    parser.add_argument(
        '--p-values',
        type=float,
        nargs='+',
        default=None,
        help='Edge probability for Erdős-Rényi random graphs (p). Each edge exists independently with probability p. If not specified, defaults to log(n)/n, n^(-1/2), 0.1, 0.2, 0.3 for each n value.'
    )
    parser.add_argument(
        '--k-values',
        type=int,
        nargs='+',
        default=None,
        help='Spanner parameter (k). The algorithm constructs a (2k-1)-spanner, meaning distances in the spanner are at most (2k-1) times the distances in the original graph. Larger k values produce sparser spanners but with higher stretch. Must be integers >= 2 and <= log(n) for all n values. If not specified, defaults are computed based on n values.'
    )
    parser.add_argument(
        '--stretch-samples',
        type=int,
        default=1000,
        help='Number of vertex pairs to sample for stretch computation. Each sample requires BFS in both original graph and spanner, so reducing this speeds up experiments. Default: 1000'
    )
    
    args = parser.parse_args()
    
    # Default parameter values
    n_values = args.n_values
    
    # Validate n values: all must be > 100
    for n in n_values:
        if n <= 100:
            raise ValueError(f"All n values must be > 100, got n={n}")
    
    # Validate and set default k values
    # k must be in range [2, floor(log(n))] for each n value
    if args.k_values is None:
        # Compute default k values: use k values that work for all n values
        # Find minimum max_k across all n values
        min_max_k = min(int(math.log(n)) for n in n_values)
        # Ensure at least k=2 is available
        if min_max_k < 2:
            raise ValueError(f"Cannot compute valid k values. min_max_k={min_max_k} < 2")
        # Default: use a reasonable range, e.g., [2, 3, 4] or up to min_max_k
        k_values = list(range(2, min(min_max_k + 1, 6)))  # At most [2, 3, 4, 5]
    else:
        k_values = args.k_values
    
    # Validate k values
    for k in k_values:
        if not isinstance(k, int) or k < 2:
            raise ValueError(f"k values must be integers >= 2, got k={k}")
    
    # Validate k values against all n values: k must be <= log(n) for each n
    for n in n_values:
        max_k = int(math.log(n))
        invalid_ks = [k for k in k_values if k > max_k]
        if invalid_ks:
            raise ValueError(f"k values {invalid_ks} are invalid for n={n}. k must be <= log({n}) = {max_k}")
    
    if args.p_values is None:
        # Default p values: log(n)/n, n^(-1/2), 0.1, 0.2, 0.3
        # We'll compute these per n value
        p_values = []
        for n in n_values:
            p_vals_for_n = [
                math.log(n) / n if n > 1 else 0.1,
                n ** (-0.5),
                0.1,
                0.2,
                0.3
            ]
            p_values.extend(p_vals_for_n)
        p_values = sorted(list(set(p_values)))  # Remove duplicates and sort
    else:
        p_values = args.p_values
    
    # Generate timestamped output filename if not provided
    if args.output is None:
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        args.output = str(output_dir / f"experiments-results-{timestamp}.csv")
    
    print("=" * 60)
    print("Baswana-Sen Spanner Experiments")
    print("=" * 60)
    print(f"n values: {n_values}")
    print(f"p values: {p_values}")
    print(f"k values: {k_values}")
    print(f"Repetitions: {args.reps}")
    print(f"Base seed: {args.seed}")
    print(f"Stretch samples: {args.stretch_samples}")
    print(f"Output: {args.output}")
    print("=" * 60)
    
    # Run experiments (saves incrementally to output file)
    df = run_experiment_suite(
        n_values=n_values,
        p_values=p_values,
        k_values=k_values,
        n_reps=args.reps,
        base_seed=args.seed,
        n_stretch_samples=args.stretch_samples,
        output_path=args.output
    )
    
    print(f"\nCompleted {len(df)} experiments.")
    print(f"Results saved to {args.output}")


if __name__ == '__main__':
    main()

