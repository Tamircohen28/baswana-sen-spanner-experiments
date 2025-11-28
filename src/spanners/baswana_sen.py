"""Baswana-Sen algorithm for constructing (2k-1)-spanners."""

from collections import deque
from typing import Dict, List, Set

import numpy as np

from ..utils.seeding import set_seed


def _bfs_distances(graph: Dict[int, List[int]], source: int) -> Dict[int, int]:
    """Compute distances from source to all reachable vertices using BFS."""
    distances = {source: 0}
    queue = deque([source])
    
    while queue:
        u = queue.popleft()
        for v in graph.get(u, []):
            if v not in distances:
                distances[v] = distances[u] + 1
                queue.append(v)
    
    return distances


def build_spanner_baswana_sen(G: Dict[int, List[int]], k: int, seed: int) -> Dict[int, List[int]]:
    """
    Build a (2k-1)-spanner using the Baswana-Sen randomized algorithm.
    
    The algorithm constructs a spanner H such that for any edge (u,v) in G,
    the distance in H is at most (2k-1) times the distance in G.
    
    Args:
        G: Input graph as adjacency list {vertex: [neighbors]}
        k: Spanner parameter (produces (2k-1)-spanner)
        seed: Random seed for reproducibility
        
    Returns:
        Spanner H as adjacency list (same format as input)
    """
    set_seed(seed)
    
    n = len(G)
    if n == 0:
        return {}
    if k <= 0:
        # For k <= 0, return empty graph (not a valid spanner, but handle gracefully)
        return {v: [] for v in G}
    if k == 1:
        # For k=1, we need a 1-spanner (exact), which is just the graph itself
        # But we can optimize: return a spanning tree for connectivity
        # Actually, for k=1, (2k-1)=1, so we need exact distances
        # A spanning tree is sufficient for connectivity, but not for exact distances
        # For simplicity, return the full graph for k=1
        return {v: list(neighbors) for v, neighbors in G.items()}
    
    # Initialize: each vertex is in its own cluster
    # clusters[i] = set of vertices in cluster i
    # cluster_id[v] = cluster id that vertex v belongs to
    clusters = {i: {i} for i in range(n)}
    cluster_id = {i: i for i in range(n)}
    
    # Spanner edges
    H = {v: [] for v in range(n)}
    
    # Phase 0: All vertices are in their own clusters (already initialized)
    
    # Phases 1 to k-1
    for phase in range(1, k):
        # Sample clusters with probability n^(-1/k)
        prob = n ** (-1.0 / k)
        sampled_clusters = set()
        
        for cluster_idx in clusters:
            if np.random.random() < prob:
                sampled_clusters.add(cluster_idx)
        
        # Build new clusters around sampled ones
        new_clusters = {}
        new_cluster_id = {}
        next_cluster_id = 0
        
        # For each sampled cluster, form a new cluster
        for old_cluster_idx in sampled_clusters:
            old_cluster = clusters[old_cluster_idx]
            new_cluster = set(old_cluster)
            
            # Add neighbors of vertices in the old cluster
            for u in old_cluster:
                for v in G.get(u, []):
                    if cluster_id[v] not in sampled_clusters:
                        new_cluster.add(v)
            
            # Assign new cluster id
            new_cluster_id_val = next_cluster_id
            next_cluster_id += 1
            new_clusters[new_cluster_id_val] = new_cluster
            
            for v in new_cluster:
                new_cluster_id[v] = new_cluster_id_val
        
        # Handle vertices not in any new cluster
        for v in range(n):
            if v not in new_cluster_id:
                # Keep in old cluster or form singleton
                old_cid = cluster_id[v]
                if old_cid not in sampled_clusters:
                    # Form new singleton cluster
                    new_cluster_id_val = next_cluster_id
                    next_cluster_id += 1
                    new_clusters[new_cluster_id_val] = {v}
                    new_cluster_id[v] = new_cluster_id_val
        
        # Add edges to maintain spanner property
        # For each edge (u,v) in G, if u and v are in different clusters,
        # add the edge to H
        for u in range(n):
            for v in G.get(u, []):
                if u < v:  # Process each edge once
                    if new_cluster_id[u] != new_cluster_id[v]:
                        # Add edge if not already present
                        if v not in H[u]:
                            H[u].append(v)
                        if u not in H[v]:
                            H[v].append(u)
        
        # Update clusters for next phase
        clusters = new_clusters
        cluster_id = new_cluster_id
    
    # Phase k: Add edges for vertices in different clusters
    # This ensures connectivity and maintains the spanner property
    for u in range(n):
        for v in G.get(u, []):
            if u < v:  # Process each edge once
                if cluster_id[u] != cluster_id[v]:
                    # Add edge if not already present
                    if v not in H[u]:
                        H[u].append(v)
                    if u not in H[v]:
                        H[v].append(u)
    
    return H

