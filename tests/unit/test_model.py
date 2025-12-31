from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph, FunctionSymbol, CodeLocation
from pathlib import Path


def test_dependency_graph_add_edge():
    id1 = SymbolId("python", "mod", "a")
    id2 = SymbolId("python", "mod", "b")

    f1 = FunctionSymbol(id=id1, name="a", module="mod", location=CodeLocation(Path("x.py"), 1, 0))
    f2 = FunctionSymbol(id=id2, name="b", module="mod", location=CodeLocation(Path("x.py"), 2, 0))

    graph = DependencyGraph()
    graph.add_node(f1)
    graph.add_node(f2)
    graph.add_edge(id1, id2)

    assert id2 in graph.edges[id1]
    assert id1 in graph.reverse_edges[id2]
