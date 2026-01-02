import tempfile
import webbrowser
from pathlib import Path

from graphviz import Digraph


def visualize_svg(dot: Digraph) -> None:
    """
    Render a Graphviz Digraph to SVG and open it.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as f:
        svg_path = Path(f.name)

    dot.render(svg_path.with_suffix(""), cleanup=True)
    webbrowser.open(svg_path.as_uri())
