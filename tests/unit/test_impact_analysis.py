from pathlib import Path

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import CodeLocation, DependencyGraph, FunctionSymbol
from pyimpact.query.engine import ImpactAnalyzer


def make_symbol(name: str) -> FunctionSymbol:
    return FunctionSymbol(
        id=SymbolId("python", "mod", name),
        name=name,
        module="mod",
        location=CodeLocation(Path("mod.py"), 1, 0),
    )


def test_downstream_impact():
    a = make_symbol("a")
    b = make_symbol("b")
    c = make_symbol("c")

    graph = DependencyGraph()
    for s in (a, b, c):
        graph.add_node(s)

    graph.add_edge(a.id, b.id)
    graph.add_edge(b.id, c.id)

    analyzer = ImpactAnalyzer(graph)
    impacted = analyzer.downstream(a.id)

    assert b.id in impacted
    assert c.id in impacted


def test_upstream_impact():
    a = make_symbol("a")
    b = make_symbol("b")
    c = make_symbol("c")

    graph = DependencyGraph()
    for s in (a, b, c):
        graph.add_node(s)

    graph.add_edge(a.id, b.id)
    graph.add_edge(b.id, c.id)

    analyzer = ImpactAnalyzer(graph)
    affecting = analyzer.upstream(c.id)

    assert b.id in affecting
    assert a.id in affecting
