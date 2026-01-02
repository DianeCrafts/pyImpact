from pathlib import Path

from pyimpact.analyzer.scanner import scan_python_files
from pyimpact.analyzer.parser import parse_python_file
from pyimpact.analyzer.graph_builder import GraphBuilder
from pyimpact.analyzer.resolver import Resolver
from pyimpact.query.engine import ImpactAnalyzer
from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph


def run_impact_analysis(
    function_name: str,
    project_root: Path,
) -> tuple[
    DependencyGraph,
    SymbolId,
    set[SymbolId],
    set[SymbolId],
]:
    """
    Run impact analysis for a given function.

    Returns:
        full_graph,
        target_symbol,
        downstream_symbols,
        upstream_symbols
    """
    builder = GraphBuilder()
    full_graph = DependencyGraph()

    # Step 1–3: Scan → Parse → Build
    for file_path in scan_python_files(project_root):
        module_name = file_path.stem
        functions, calls, imports = parse_python_file(file_path)

        graph = builder.build(
            file_path=file_path,
            module_name=module_name,
            functions=functions,
            calls=calls,
            imports=imports,
        )

        full_graph.nodes.update(graph.nodes)

        for k, v in graph.edges.items():
            full_graph.edges.setdefault(k, set()).update(v)

        for k, v in graph.reverse_edges.items():
            full_graph.reverse_edges.setdefault(k, set()).update(v)

        full_graph.unresolved_calls.extend(graph.unresolved_calls)

    if not full_graph.nodes:
        raise ValueError("No Python functions found in project")

    # Step 4: Resolve
    Resolver().resolve(full_graph)

    # Step 5: Find target
    matches = [sid for sid in full_graph.nodes if sid.qualname == function_name]

    if not matches:
        raise ValueError(f"Function '{function_name}' not found")

    if len(matches) > 1:
        raise ValueError(
            f"Function name '{function_name}' is ambiguous. "
            f"Please use a qualified name."
        )

    target_id = matches[0]

    # Step 6: Impact analysis
    analyzer = ImpactAnalyzer(full_graph)
    downstream = analyzer.downstream(target_id)
    upstream = analyzer.upstream(target_id)

    return full_graph, target_id, downstream, upstream
