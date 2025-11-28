"""Erdős–Rényi graph generation."""

from collections import deque
from typing import Dict, List, Tuple

import numpy as np

from ..utils.seeding import set_seed


def _bfs_component(graph: Dict[int, List[int]], start: int, visited: set) -> List[int]:
    """Find connected component using BFS starting from start vertex."""
    component = []
    queue = deque([start])
    visited.add(start)
    
    while queue:
        v = queue.popleft()
        component.append(v)
        for neighbor in graph.get(v, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return component


def _extract_largest_component(graph: Dict[int, List[int]]) -> Tuple[Dict[int, List[int]], int, int]:
    """
    Extract the largest connected component from a graph.
    
    Args:
        graph: Adjacency list representation
        
    Returns:
        Tuple of (component_graph, n_original, n_connected)
    """
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = _bfs_component(graph, vertex, visited)
            components.append(component)
    
    if not components:
        return {}, len(graph), 0
    
    # Find largest component
    largest_component = max(components, key=len)
    largest_set = set(largest_component)
    
    # Create mapping from old vertex labels to new (0..n-1)
    vertex_map = {old_v: new_v for new_v, old_v in enumerate(largest_component)}
    
    # Build new graph with relabeled vertices
    component_graph = {}
    for old_v in largest_component:
        new_v = vertex_map[old_v]
        component_graph[new_v] = []
        for neighbor in graph[old_v]:
            if neighbor in largest_set:
                component_graph[new_v].append(vertex_map[neighbor])
    
    return component_graph, len(graph), len(largest_component)


def generate_erdos_renyi_graph(n: int, p: float, seed: int) -> Tuple[Dict[int, List[int]], int, int]:
    """
    Generate an Erdős–Rényi random graph G(n, p).
    
    Each pair of vertices is connected with probability p independently.
    Returns the largest connected component with vertices relabeled 0..(n_cc-1).
    
    Args:
        n: Number of vertices
        p: Edge probability (0 <= p <= 1)
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (graph_dict, n_original, n_connected) where:
        - graph_dict: Adjacency list {vertex: [neighbors]}
        - n_original: Original number of vertices
        - n_connected: Number of vertices in largest component
    """
    set_seed(seed)
    
    # Initialize empty graph
    graph = {i: [] for i in range(n)}
    
    # Generate edges: for each pair (i, j) with i < j, add edge with probability p
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.random() < p:
                graph[i].append(j)
                graph[j].append(i)
    
    # Extract largest connected component
    component_graph, n_original, n_connected = _extract_largest_component(graph)
    
    return component_graph, n_original, n_connected

