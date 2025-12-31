from pathlib import Path

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import (
    CallSite,
    CodeLocation,
    DependencyGraph,
    FunctionSymbol,
)
from pyimpact.analyzer.resolver import Resolver


def test_resolver_links_cross_file_calls():
    graph = DependencyGraph()

    parser_fn = FunctionSymbol(
        id=SymbolId("python", "parser", "parse_python_file"),
        name="parse_python_file",
        module="parser",
        location=CodeLocation(Path("parser.py"), 1, 0),
    )

    impact_fn = FunctionSymbol(
        id=SymbolId("python", "impact", "run_impact_analysis"),
        name="run_impact_analysis",
        module="impact",
        location=CodeLocation(Path("impact.py"), 1, 0),
    )

    graph.add_node(parser_fn)
    graph.add_node(impact_fn)

    graph.unresolved_calls.append(
        CallSite(
            caller_id=impact_fn.id,
            callee_name="parse_python_file",
            callee_id=None,
            location=CodeLocation(Path("impact.py"), 2, 4),
        )
    )

    Resolver().resolve(graph)

    assert parser_fn.id in graph.edges[impact_fn.id]
