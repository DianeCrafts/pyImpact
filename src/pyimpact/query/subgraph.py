from enum import Enum
from typing import Dict, Set, Tuple

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph
from pyimpact.query.engine import ImpactAnalyzer


class SubgraphMode(str, Enum):
    IMPACT = "impact"
    CALLERS = "callers"
    CALLEES = "callees"


def extract_subgraph(
    graph: DependencyGraph,
    target: SymbolId,
    mode: SubgraphMode,
) -> tuple[
    Set[SymbolId],
    Set[tuple[SymbolId, SymbolId]],
    Dict[SymbolId, str],
]:
    """
    Extract a focused subgraph for visualization.

    Returns:
        nodes: symbols to include
        edges: edges between those symbols
        roles: mapping SymbolId -> role (target/upstream/downstream)
    """
    analyzer = ImpactAnalyzer(graph)

    if mode == SubgraphMode.IMPACT:
        upstream = analyzer.upstream(target)
        downstream = analyzer.downstream(target)
    elif mode == SubgraphMode.CALLERS:
        upstream = analyzer.upstream(target)
        downstream = set()
    elif mode == SubgraphMode.CALLEES:
        upstream = set()
        downstream = analyzer.downstream(target)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    nodes = upstream | downstream | {target}
    edges: Set[tuple[SymbolId, SymbolId]] = set()

    for caller, callees in graph.edges.items():
        for callee in callees:
            if caller in nodes and callee in nodes:
                edges.add((caller, callee))

    roles: Dict[SymbolId, str] = {}
    for n in nodes:
        if n == target:
            roles[n] = "target"
        elif n in upstream:
            roles[n] = "upstream"
        elif n in downstream:
            roles[n] = "downstream"

    return nodes, edges, roles
