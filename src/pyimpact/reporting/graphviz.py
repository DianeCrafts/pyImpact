from graphviz import Digraph
from pyimpact.core.ids import SymbolId


def _node_id(symbol: SymbolId) -> str:
    """
    Generate a Graphviz-safe node ID.
    """
    return f"{symbol.language}_{symbol.module}_{symbol.qualname}".replace(".", "_")


def render_svg(
    nodes: set[SymbolId],
    edges: set[tuple[SymbolId, SymbolId]],
    roles: dict[SymbolId, str],
) -> Digraph:
    dot = Digraph("PyImpact", format="svg")
    dot.attr(rankdir="LR")

    # Add nodes
    for node in nodes:
        role = roles.get(node)

        if role == "target":
            color = "red"
            style = "filled"
        elif role == "upstream":
            color = "lightblue"
            style = "filled"
        elif role == "downstream":
            color = "lightgreen"
            style = "filled"
        else:
            color = "gray"
            style = "solid"

        dot.node(
            name=_node_id(node),
            label=f"{node.module}.{node.qualname}",
            color=color,
            style=style,
        )

    # Add edges
    for src, dst in edges:
        dot.edge(_node_id(src), _node_id(dst))

    return dot
