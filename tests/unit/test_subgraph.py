from pathlib import Path

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph, FunctionSymbol, CodeLocation
from pyimpact.query.subgraph import extract_subgraph


def _make_symbol(name: str) -> FunctionSymbol:
    return FunctionSymbol(
        id=SymbolId("python", "mod", name),
        name=name,
        module="mod",
        location=CodeLocation(Path("mod.py"), 1, 0),
    )


def test_extract_subgraph_filters_nodes_and_edges():
    """
    Only upstream, target, and downstream nodes should appear.
    Unrelated nodes must be excluded.
    """
    graph = DependencyGraph()

    a = _make_symbol("a")
    b = _make_symbol("b")
    c = _make_symbol("c")
    d = _make_symbol("d")  # unrelated

    for s in (a, b, c, d):
        graph.add_node(s)

    graph.add_edge(a.id, b.id)
    graph.add_edge(b.id, c.id)
    graph.add_edge(d.id, a.id)  # unrelated path

    nodes, edges = extract_subgraph(
        graph=graph,
        target=b.id,
        upstream={a.id},
        downstream={c.id},
    )

    # Nodes
    assert a.id in nodes
    assert b.id in nodes
    assert c.id in nodes
    assert d.id not in nodes

    # Edges
    assert (a.id, b.id) in edges
    assert (b.id, c.id) in edges
    assert (d.id, a.id) not in edges
