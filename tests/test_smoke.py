"""Smoke tests for baswana-sen-spanner-experiments."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_imports():
    from src.spanners.baswana_sen import build_spanner_baswana_sen
    from src.spanners.greedy import build_greedy_spanner
    from src.graphs.erdos_renyi import generate_erdos_renyi_graph

    assert callable(build_spanner_baswana_sen)
    assert callable(build_greedy_spanner)
    assert callable(generate_erdos_renyi_graph)


def test_baswana_sen_small_graph():
    from src.spanners.baswana_sen import build_spanner_baswana_sen

    graph = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
    }
    spanner = build_spanner_baswana_sen(graph, k=2, seed=42)
    assert len(spanner) == 3
    assert all(u in spanner for u in graph)
