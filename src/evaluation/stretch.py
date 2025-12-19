"""Stretch computation utilities for spanner evaluation."""

from collections import deque
from typing import Dict, List, Tuple

import numpy as np


def compute_distances_bfs(G: Dict[int, List[int]], source: int) -> Dict[int, int]:
    """
    Compute distances from source to all reachable vertices using BFS.
    
    Args:
        G: Graph as adjacency list
        source: Source vertex
        
    Returns:
        Dictionary mapping vertex to distance from source
    """
    distances = {source: 0}
    queue = deque[int]([source])
    
    while queue:
        u = queue.popleft()
        for v in G.get(u, []):
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    
    return distances


def compute_all_pairs_distances(G: Dict[int, List[int]]) -> Dict[Tuple[int, int], int]:
    """
    Compute all-pairs shortest distances in a graph.
    
    Args:
        G: Graph as adjacency list
        
    Returns:
        Dictionary mapping (u, v) pairs to distance (only u < v to avoid duplicates)
    """
    all_distances = {}
    n = len(G)
    
    for source in range(n):
        distances = compute_distances_bfs(G, source)
        for target, dist in distances.items():
            if source < target:
                all_distances[(source, target)] = dist
            elif target < source:
                all_distances[(target, source)] = dist
    
    return all_distances


def compute_stretch_edges(G: Dict[int, List[int]], H: Dict[int, List[int]]) -> Dict:
    """
    Compute stretch for all edges in G.
    
    For each edge (u,v) in G, stretch = d_H(u,v) / d_G(u,v).
    
    Args:
        G: Original graph
        H: Spanner graph
        
    Returns:
        Dictionary with keys:
        - 'max_stretch': Maximum stretch over all edges
        - 'avg_stretch': Average stretch over all edges
        - 'stretches': List of all stretch values
        - 'n_edges': Number of edges processed
    """
    stretches = []
    
    # Compute distances in H
    dist_H = compute_all_pairs_distances(H)
    
    # For each edge (u,v) in G
    for u in G:
        for v in G.get(u, []):
            if u < v:  # Process each edge once
                # Distance in G is 1 (it's an edge)
                d_G = 1
                
                # Distance in H
                if (u, v) in dist_H:
                    d_H = dist_H[(u, v)]
                elif u == v:
                    d_H = 0
                else:
                    # Check if reachable in H
                    dists_from_u = compute_distances_bfs(H, u)
                    if v in dists_from_u:
                        d_H = dists_from_u[v]
                    else:
                        # Unreachable - infinite stretch
                        d_H = float('inf')
                
                if d_H == float('inf'):
                    stretch = float('inf')
                else:
                    stretch = d_H / d_G if d_G > 0 else float('inf')
                
                stretches.append(stretch)
    
    if not stretches:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_edges': 0}
    
    # Filter out infinite stretches for average calculation
    finite_stretches = [s for s in stretches if s != float('inf')]
    
    max_stretch = max(stretches) if stretches else 0.0
    avg_stretch = sum(finite_stretches) / len(finite_stretches) if finite_stretches else 0.0
    
    return {'max_stretch': max_stretch if max_stretch != float('inf') else float('inf'), 'avg_stretch': avg_stretch, 'stretches': stretches, 'n_edges': len(stretches), 'n_infinite': len(stretches) - len(finite_stretches)}


def compute_stretch_sampled_edges(G: Dict[int, List[int]], H: Dict[int, List[int]], n_samples: int, seed: int = None) -> Dict:
    """
    Compute stretch for a sample of edges in G.
    
    For each sampled edge (u,v) in G, stretch = d_H(u,v) / d_G(u,v).
    This is a memory-efficient alternative to compute_stretch_edges for large graphs.
    
    Args:
        G: Original graph
        H: Spanner graph
        n_samples: Number of edges to sample
        seed: Random seed for sampling
        
    Returns:
        Dictionary with keys:
        - 'max_stretch': Maximum stretch over sampled edges
        - 'avg_stretch': Average stretch over sampled edges
        - 'stretches': List of stretch values
        - 'n_edges': Number of edges processed
    """
    if seed is not None:
        np.random.seed(seed)
    
    n = len(G)
    if n < 2:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_edges': 0, 'n_infinite': 0}
    
    # Collect all edges in G
    edges = []
    for u in G:
        for v in G.get(u, []):
            if u < v:  # Process each edge once
                edges.append((u, v))
    
    if not edges:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_edges': 0, 'n_infinite': 0}
    
    # Sample edges
    n_samples = min(n_samples, len(edges))
    sampled_edges = [edges[i] for i in np.random.choice(len(edges), size=n_samples, replace=False)]
    
    stretches = []
    
    # For each sampled edge (u,v) in G
    for u, v in sampled_edges:
        # Distance in G is 1 (it's an edge)
        d_G = 1
        
        # Compute distance in H using targeted BFS
        dists_H = compute_distances_bfs(H, u)
        if v not in dists_H:
            # Unreachable in H - infinite stretch
            d_H = float('inf')
        else:
            d_H = dists_H[v]
        
        if d_H == float('inf'):
            stretch = float('inf')
        else:
            stretch = d_H / d_G if d_G > 0 else float('inf')
        
        stretches.append(stretch)
    
    if not stretches:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_edges': 0, 'n_infinite': 0}
    
    # Filter out infinite stretches for average calculation
    finite_stretches = [s for s in stretches if s != float('inf')]
    
    max_stretch = max(stretches) if stretches else 0.0
    avg_stretch = sum(finite_stretches) / len(finite_stretches) if finite_stretches else 0.0
    
    return {'max_stretch': max_stretch if max_stretch != float('inf') else float('inf'), 'avg_stretch': avg_stretch, 'stretches': stretches, 'n_edges': len(stretches), 'n_infinite': len(stretches) - len(finite_stretches)}


def compute_stretch_sampled_pairs(G: Dict[int, List[int]], H: Dict[int, List[int]], n_samples: int, seed: int = None) -> Dict:
    """
    Compute stretch for a sample of vertex pairs.
    
    Args:
        G: Original graph
        H: Spanner graph
        n_samples: Number of vertex pairs to sample
        seed: Random seed for sampling
        
    Returns:
        Dictionary with keys:
        - 'max_stretch': Maximum stretch over sampled pairs
        - 'avg_stretch': Average stretch over sampled pairs
        - 'stretches': List of stretch values
        - 'n_pairs': Number of pairs processed
    """
    if seed is not None:
        np.random.seed(seed)
    
    n = len(G)
    if n < 2:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_pairs': 0}
    
    stretches = []
    
    # Sample pairs
    for _ in range(n_samples):
        u = np.random.randint(0, n)
        v = np.random.randint(0, n)
        
        # Skip self-loops
        if u == v:
            continue
        
        # Ensure u < v for consistency
        if u > v:
            u, v = v, u
        
        # Compute distance in G
        dists_G = compute_distances_bfs(G, u)
        if v not in dists_G:
            # Unreachable in G - skip
            continue
        d_G = dists_G[v]
        
        if d_G == 0:
            continue
        
        # Compute distance in H
        dists_H = compute_distances_bfs(H, u)
        if v not in dists_H:
            # Unreachable in H - infinite stretch
            stretch = float('inf')
        else:
            d_H = dists_H[v]
            stretch = d_H / d_G if d_G > 0 else float('inf')
        
        stretches.append(stretch)
    
    if not stretches:
        return {'max_stretch': 0.0, 'avg_stretch': 0.0, 'stretches': [], 'n_pairs': 0}
    
    # Filter out infinite stretches for average
    finite_stretches = [s for s in stretches if s != float('inf')]
    
    max_stretch = max(stretches) if stretches else 0.0
    avg_stretch = sum(finite_stretches) / len(finite_stretches) if finite_stretches else 0.0
    
    return {
        'max_stretch': max_stretch if max_stretch != float('inf') else float('inf'),
        'avg_stretch': avg_stretch,
        'stretches': stretches,
        'n_pairs': len(stretches),
        'n_infinite': len(stretches) - len(finite_stretches)
    }

