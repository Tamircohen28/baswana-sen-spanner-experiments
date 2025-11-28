#!/usr/bin/env python3
"""Command-line script to run all spanner experiments."""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.experiments import run_experiment_suite, save_results


def main():
    """Main entry point for experiment runner."""
    parser = argparse.ArgumentParser(
        description='Run Baswana-Sen spanner experiments'
    )
    parser.add_argument(
        '--max-n',
        type=int,
        default=50000,
        help='Maximum n value (default: 50000)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/processed/experiments_full.csv',
        help='Output CSV path (default: data/processed/experiments_full.csv)'
    )
    parser.add_argument(
        '--reps',
        type=int,
        default=10,
        help='Number of repetitions per combination (default: 10)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Base random seed (default: 42)'
    )
    parser.add_argument(
        '--n-values',
        type=int,
        nargs='+',
        default=None,
        help='Custom n values (overrides default: 5000, 10000, 20000, 50000)'
    )
    parser.add_argument(
        '--p-values',
        type=float,
        nargs='+',
        default=None,
        help='Custom p values (overrides default)'
    )
    parser.add_argument(
        '--k-values',
        type=int,
        nargs='+',
        default=None,
        help='Custom k values (overrides default: 1, 2, 3, 4, 5)'
    )
    parser.add_argument(
        '--stretch-samples',
        type=int,
        default=10000,
        help='Number of pairs to sample for stretch computation (default: 10000)'
    )
    
    args = parser.parse_args()
    
    # Default parameter values
    if args.n_values is None:
        n_values = [n for n in [5000, 10000, 20000, 50000] if n <= args.max_n]
    else:
        n_values = [n for n in args.n_values if n <= args.max_n]
    
    if args.p_values is None:
        # Default p values: log(n)/n, n^(-1/2), 0.1, 0.2, 0.3
        # We'll compute these per n value
        import math
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
    
    if args.k_values is None:
        k_values = [1, 2, 3, 4, 5]
    else:
        k_values = args.k_values
    
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
    
    # Run experiments
    df = run_experiment_suite(
        n_values=n_values,
        p_values=p_values,
        k_values=k_values,
        n_reps=args.reps,
        base_seed=args.seed,
        n_stretch_samples=args.stretch_samples
    )
    
    # Save results
    save_results(df, args.output)
    
    print(f"\nCompleted {len(df)} experiments.")
    print(f"Results saved to {args.output}")


if __name__ == '__main__':
    main()

