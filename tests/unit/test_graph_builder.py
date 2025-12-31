from pathlib import Path

from pyimpact.analyzer.graph_builder import GraphBuilder
from pyimpact.analyzer.parser import FunctionDefInfo, CallSiteInfo


def test_graph_builder_creates_nodes_and_edges():
    builder = GraphBuilder()

    functions = [
        FunctionDefInfo(name="a", lineno=1, col_offset=0),
        FunctionDefInfo(name="b", lineno=5, col_offset=0),
    ]

    calls = [
        CallSiteInfo(caller="a", callee="b", lineno=2, col_offset=4),
        CallSiteInfo(caller="a", callee="c", lineno=3, col_offset=4),
    ]

    graph = builder.build(
        file_path=Path("mod.py"),
        module_name="mod",
        functions=functions,
        calls=calls,
    )

    ids = list(graph.nodes.keys())
    id_map = {id.qualname: id for id in ids}

    assert "a" in id_map
    assert "b" in id_map

    a_id = id_map["a"]
    b_id = id_map["b"]

    assert b_id in graph.edges[a_id]
    assert a_id in graph.reverse_edges[b_id]


def test_graph_builder_ignores_unresolved_calls():
    builder = GraphBuilder()

    functions = [FunctionDefInfo(name="a", lineno=1, col_offset=0)]
    calls = [CallSiteInfo(caller="a", callee="missing", lineno=2, col_offset=4)]

    graph = builder.build(
        file_path=Path("mod.py"),
        module_name="mod",
        functions=functions,
        calls=calls,
    )

    a_id = next(iter(graph.nodes))
    assert graph.edges[a_id] == set()
