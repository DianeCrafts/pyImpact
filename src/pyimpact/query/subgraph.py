from typing import Set

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph


def extract_subgraph(
    graph: DependencyGraph,
    target: SymbolId,
    upstream: Set[SymbolId],
    downstream: Set[SymbolId],
) -> tuple[
    Set[SymbolId],
    Set[tuple[SymbolId, SymbolId]],
]:
    """
    Extract a focused subgraph for visualization.
    """
    nodes = upstream | downstream | {target}
    edges: Set[tuple[SymbolId, SymbolId]] = set()

    for caller, callees in graph.edges.items():
        for callee in callees:
            if caller in nodes and callee in nodes:
                edges.add((caller, callee))

    return nodes, edges
