from pathlib import Path
from typing import Iterable

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import (
    CallSite,
    CodeLocation,
    DependencyGraph,
    FunctionSymbol,
)
from pyimpact.analyzer.parser import (
    FunctionDefInfo,
    CallSiteInfo,
    ImportInfo,
)


class GraphBuilder:
    """
    Builds a DependencyGraph from parsed source files.

    This class is language-agnostic at the graph level.
    Language-specific parsing happens before this stage.
    """

    def __init__(self, language: str = "python") -> None:
        self.language = language

    def build(
        self,
        file_path: Path,
        module_name: str,
        functions: Iterable[FunctionDefInfo],
        calls: Iterable[CallSiteInfo],
        imports: Iterable[ImportInfo],
    ) -> DependencyGraph:
        """
        Build a dependency graph for a single module.

        Args:
            file_path: Path to the source file
            module_name: Logical module name (e.g. pyimpact.analyzer.parser)
            functions: Parsed function definitions
            calls: Parsed call sites
            imports: Parsed import statements

        Returns:
            DependencyGraph containing:
            - nodes for function definitions
            - edges for resolved calls
            - unresolved_calls for later resolution
        """
        graph = DependencyGraph()

        # --------------------------------------------------
        # Step 1: create function symbols (nodes)
        # --------------------------------------------------
        name_to_symbol: dict[str, SymbolId] = {}

        for fn in functions:
            symbol_id = SymbolId(
                language=self.language,
                module=module_name,
                qualname=fn.name,
            )

            symbol = FunctionSymbol(
                id=symbol_id,
                name=fn.name,
                module=module_name,
                location=CodeLocation(
                    file_path=file_path,
                    line=fn.lineno,
                    column=fn.col_offset,
                ),
            )

            graph.add_node(symbol)
            name_to_symbol[fn.name] = symbol_id

        # --------------------------------------------------
        # Step 2: add edges for call sites
        # --------------------------------------------------
        for call in calls:
            caller_id = name_to_symbol.get(call.caller)
            if caller_id is None:
                # Call outside a known function — ignore
                continue

            callee_id = name_to_symbol.get(call.callee)

            call_site = CallSite(
                caller_id=caller_id,
                callee_name=call.callee,
                callee_id=callee_id,
                location=CodeLocation(
                    file_path=file_path,
                    line=call.lineno,
                    column=call.col_offset,
                ),
            )

            if callee_id:
                # Resolved inside the same module
                graph.add_edge(caller_id, callee_id)
            else:
                # Cross-file or unresolved — resolver will handle it
                graph.unresolved_calls.append(call_site)

        return graph
