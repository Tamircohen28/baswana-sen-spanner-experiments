"""Metrics and statistics utilities for experiment results."""

import pandas as pd


def aggregate_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate experiment results by grouping on (n, p, k).
    
    Computes mean, std, min, max for key metrics.
    
    Args:
        df: DataFrame with experiment results
        
    Returns:
        Aggregated DataFrame with statistics grouped by (n, p, k)
    """
    if df.empty:
        return df
    
    # Key metrics to aggregate
    metrics = [
        'spanner_size',
        'spanner_size_ratio',
        'max_stretch_edges',
        'avg_stretch_edges',
        'max_stretch_pairs',
        'avg_stretch_pairs',
        'time_gen',
        'time_spanner',
        'time_stretch'
    ]
    
    # Filter to only existing columns
    metrics = [m for m in metrics if m in df.columns]
    
    # Group by (n, p, k)
    grouped = df.groupby(['n', 'p', 'k'])
    
    # Compute statistics
    agg_dict = {}
    for metric in metrics:
        agg_dict[metric] = ['mean', 'std', 'min', 'max']
    
    if agg_dict:
        aggregated = grouped[metrics].agg(agg_dict)
    else:
        # If no metrics, just return groupby object with count
        aggregated = grouped.size().to_frame('count')
    
    # Flatten column names
    aggregated.columns = ['_'.join(col).strip() if col[1] else col[0] 
                         for col in aggregated.columns.values]
    
    # Reset index
    aggregated = aggregated.reset_index()
    
    return aggregated


def compute_theoretical_bound(n: int, k: int) -> float:
    """
    Compute theoretical bound O(k * n^(1+1/k)) for spanner size.
    
    Args:
        n: Number of vertices
        k: Spanner parameter
        
    Returns:
        Theoretical bound value
    """
    return k * (n ** (1 + 1.0 / k))

