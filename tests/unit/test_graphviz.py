from pyimpact.core.ids import SymbolId
from pyimpact.reporting.graphviz import render_svg


def test_graphviz_node_ids_are_safe():
    """
    Graphviz node IDs must not contain ':' or other port syntax.
    """
    sid = SymbolId("python", "parser", "parse_python_file")

    dot = render_svg(
        nodes={sid},
        edges=set(),
        roles={sid: "target"},
    )

    source = dot.source

    # Graphviz treats ':' as port syntax — must not appear in IDs
    assert ":" not in source
