from graphviz import Digraph

from pyimpact.core.ids import SymbolId


def render_svg(
    nodes: set[SymbolId],
    edges: set[tuple[SymbolId, SymbolId]],
    roles: dict[SymbolId, str],
) -> Digraph:
    """
    Render a Graphviz Digraph object with styling.
    """
    dot = Digraph("PyImpact", format="svg")
    dot.attr(rankdir="LR")

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
            name=str(node),
            label=node.qualname,
            color=color,
            style=style,
        )

    for src, dst in edges:
        dot.edge(str(src), str(dst))

    return dot
