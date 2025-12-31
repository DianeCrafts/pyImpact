from pathlib import Path

from pyimpact.analyzer.scanner import scan_python_files
from pyimpact.analyzer.parser import parse_python_file
from pyimpact.analyzer.graph_builder import GraphBuilder
from pyimpact.query.engine import ImpactAnalyzer
from pyimpact.core.ids import SymbolId


def run_impact_analysis(
    function_name: str,
    project_root: Path,
) -> tuple[set[SymbolId], set[SymbolId]]:
    """
    Run impact analysis for a given function name in a project.

    Returns:
        downstream_impact, upstream_impact
    """
    builder = GraphBuilder()
    full_graph = None

    for file_path in scan_python_files(project_root):
        module_name = file_path.stem  # naive for now, improves later

        functions, calls = parse_python_file(file_path)
        graph = builder.build(file_path, module_name, functions, calls)

        if full_graph is None:
            full_graph = graph
        else:
            # merge graphs
            full_graph.nodes.update(graph.nodes)
            for k, v in graph.edges.items():
                full_graph.edges.setdefault(k, set()).update(v)
            for k, v in graph.reverse_edges.items():
                full_graph.reverse_edges.setdefault(k, set()).update(v)

    if full_graph is None:
        raise ValueError("No Python files found")

    # Find symbol ID by function name (simple version)
    target_id = next(
        (sid for sid in full_graph.nodes if sid.qualname == function_name),
        None,
    )

    if target_id is None:
        raise ValueError(f"Function '{function_name}' not found")

    analyzer = ImpactAnalyzer(full_graph)

    downstream = analyzer.downstream(target_id)
    upstream = analyzer.upstream(target_id)

    return downstream, upstream
