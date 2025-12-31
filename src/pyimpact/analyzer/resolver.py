from pyimpact.core.model import DependencyGraph
from pyimpact.core.ids import SymbolId


class Resolver:
    """
    Resolves unresolved call sites using import information.
    """

    def resolve(self, graph: DependencyGraph) -> None:
        """
        Mutates the graph by resolving unresolved call sites
        into concrete edges when possible.
        """
        for call in list(graph.unresolved_calls):
            resolved_id = self._resolve_call(call, graph)
            if resolved_id:
                graph.add_edge(call.caller_id, resolved_id)
                graph.unresolved_calls.remove(call)

    def _resolve_call(
        self,
        call,
        graph: DependencyGraph,
    ) -> SymbolId | None:
        """
        Attempt to resolve a call to a known symbol.
        """
        for symbol_id in graph.nodes:
            if symbol_id.qualname == call.callee_name:
                return symbol_id
        return None
