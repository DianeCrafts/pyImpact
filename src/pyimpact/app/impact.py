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
) -> tuple[set[SymbolId], set[SymbolId]]:
    """
    Run impact analysis for a given function in a project directory.

    This function orchestrates:
    - scanning
    - parsing
    - graph construction
    - call resolution
    - impact queries
    """
    builder = GraphBuilder()
    full_graph = DependencyGraph()

    # --------------------------------------------------
    # Step 1–3: Scan → Parse → Build graphs
    # --------------------------------------------------
    for file_path in scan_python_files(project_root):
        module_name = file_path.stem  # naive, improved later

        functions, calls, imports = parse_python_file(file_path)
        graph = builder.build(
            file_path=file_path,
            module_name=module_name,
            functions=functions,
            calls=calls,
            imports=imports,
        )

        # Merge module graph into global graph
        full_graph.nodes.update(graph.nodes)

        for k, v in graph.edges.items():
            full_graph.edges.setdefault(k, set()).update(v)

        for k, v in graph.reverse_edges.items():
            full_graph.reverse_edges.setdefault(k, set()).update(v)

        full_graph.unresolved_calls.extend(graph.unresolved_calls)

    if not full_graph.nodes:
        raise ValueError("No Python functions found in project")

    # --------------------------------------------------
    # STEP 4 — Resolve cross-file calls (THIS IS THE KEY)
    # --------------------------------------------------
    resolver = Resolver()
    resolver.resolve(full_graph)

    # --------------------------------------------------
    # Step 5: Locate target symbol
    # --------------------------------------------------
    matches = [
        sid for sid in full_graph.nodes
        if sid.qualname == function_name
    ]

    if not matches:
        raise ValueError(f"Function '{function_name}' not found")

    if len(matches) > 1:
        raise ValueError(
            f"Function name '{function_name}' is ambiguous. "
            f"Please use a qualified name."
        )

    target_id = matches[0]

    # --------------------------------------------------
    # Step 6: Impact analysis
    # --------------------------------------------------
    analyzer = ImpactAnalyzer(full_graph)

    downstream = analyzer.downstream(target_id)
    upstream = analyzer.upstream(target_id)

    return downstream, upstream
