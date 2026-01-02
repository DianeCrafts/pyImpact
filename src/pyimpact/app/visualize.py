import tempfile
import webbrowser
from pathlib import Path

from pyimpact.analyzer.scanner import scan_python_files
from pyimpact.analyzer.parser import parse_python_file
from pyimpact.analyzer.graph_builder import GraphBuilder
from pyimpact.analyzer.resolver import Resolver
from pyimpact.core.model import DependencyGraph
from pyimpact.query.subgraph import SubgraphMode, extract_subgraph
from pyimpact.reporting.graphviz import render_svg


def visualize(
    function_name: str,
    project_root: Path,
    mode: SubgraphMode,
) -> None:
    """
    Generate and immediately open a visual dependency graph.
    """
    builder = GraphBuilder()
    graph = DependencyGraph()

    for file_path in scan_python_files(project_root):
        functions, calls, imports = parse_python_file(file_path)
        module_graph = builder.build(
            file_path,
            file_path.stem,
            functions,
            calls,
            imports,
        )

        graph.nodes.update(module_graph.nodes)
        graph.edges.update(module_graph.edges)
        graph.reverse_edges.update(module_graph.reverse_edges)
        graph.unresolved_calls.extend(module_graph.unresolved_calls)

    Resolver().resolve(graph)

    matches = [sid for sid in graph.nodes if sid.qualname == function_name]
    if not matches:
        raise ValueError(f"Function '{function_name}' not found")
    if len(matches) > 1:
        raise ValueError(f"Function '{function_name}' is ambiguous")

    target = matches[0]

    nodes, edges, roles = extract_subgraph(graph, target, mode)
    dot = render_svg(nodes, edges, roles)

    # Write to a temp file and open
    with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as f:
        svg_path = Path(f.name)

    dot.render(svg_path.with_suffix(""), cleanup=True)

    webbrowser.open(svg_path.as_uri())
