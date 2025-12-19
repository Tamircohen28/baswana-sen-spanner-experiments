"""Greedy Spanner Algorithm (Althofer et al., 1993).

This implementation serves as a deterministic baseline for comparing
against the randomized Baswana-Sen algorithm. It constructs a t-spanner
by processing edges in non-decreasing order of weight (or arbitrary order
for unweighted graphs) and adding an edge (u,v) only if the current
shortest path between u and v in the spanner exceeds t * weight(u,v).
"""

from collections import deque
from typing import Dict, List


def _bfs_distance(graph: Dict[int, List[int]], start: int, target: int, limit: int) -> int:
    """
    Compute BFS distance from start to target, stopping if distance exceeds limit.
    Returns float('inf') if target is not reachable within limit.
    """
    if start == target:
        return 0
    
    # Bidirectional BFS could be faster, but simple BFS is sufficient for baseline
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        u, dist = queue.popleft()
        
        if dist >= limit:
            continue
            
        for v in graph.get(u, []):
            if v == target:
                return dist + 1
            
            if v not in visited:
                visited.add(v)
                queue.append((v, dist + 1))
    
    return float('inf')


def build_greedy_spanner(G: Dict[int, List[int]], k: int) -> Dict[int, List[int]]:
    """
    Construct a (2k-1)-spanner using the Greedy algorithm.
    
    Args:
        G: Input graph (adjacency list). Assumed unweighted for this implementation.
        k: Integer parameter, target stretch is 2k-1.
        
    Returns:
        Spanner H as adjacency list.
    """
    n = len(G)
    if n == 0:
        return {}
    
    # Initialize empty spanner
    H = {v: [] for v in G}
    
    # Extract all edges. Since undirected, store as sorted tuples (u, v) where u < v
    edges = []
    for u in G:
        for v in G[u]:
            if u < v:
                edges.append((u, v))
    
    # For weighted graphs, we would sort edges here. 
    # For unweighted, arbitrary order (or random shuffle) is fine.
    # We keep it deterministic based on vertex indices for reproducibility.
    
    stretch_limit = 2 * k - 1
    
    for u, v in edges:
        # Check distance in current spanner H
        # We only need to know if dist_H(u,v) > stretch_limit * 1
        dist = _bfs_distance(H, u, v, stretch_limit)
        
        if dist > stretch_limit:
            # Add edge to spanner
            H[u].append(v)
            H[v].append(u)
            
    return H

