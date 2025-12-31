from pathlib import Path
from typing import Iterable

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import (
    CallSite,
    CodeLocation,
    DependencyGraph,
    FunctionSymbol,
)
from pyimpact.analyzer.parser import FunctionDefInfo, CallSiteInfo


class GraphBuilder:
    """
    Builds a DependencyGraph from parsed source files.
    """

    def __init__(self, language: str = "python") -> None:
        self.language = language

    def build(
        self,
        file_path: Path,
        module_name: str,
        functions: Iterable[FunctionDefInfo],
        calls: Iterable[CallSiteInfo],
    ) -> DependencyGraph:
        """
        Build a dependency graph for a single module.

        Args:
            file_path: Path to the source file
            module_name: Logical module name (e.g. src.service.user)
            functions: Parsed function definitions
            calls: Parsed call sites

        Returns:
            DependencyGraph
        """
        graph = DependencyGraph()

        # Step 1: create function symbols
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

        # Step 2: add edges for calls
        for call in calls:
            caller_id = name_to_symbol.get(call.caller)
            if caller_id is None:
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

            # Only add edge if callee resolved in same module
            if callee_id:
                graph.add_edge(caller_id, callee_id)

        return graph
