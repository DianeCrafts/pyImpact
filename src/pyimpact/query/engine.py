from collections import deque
from typing import Set

from pyimpact.core.ids import SymbolId
from pyimpact.core.model import DependencyGraph


class ImpactAnalyzer:
    """
    Provides impact analysis queries over a dependency graph.
    """

    def __init__(self, graph: DependencyGraph) -> None:
        self.graph = graph

    def downstream(self, symbol_id: SymbolId) -> Set[SymbolId]:
        """
        Find all symbols that are affected if `symbol_id` breaks.
        (Traverse caller → callee)
        """
        visited: Set[SymbolId] = set()
        queue = deque([symbol_id])

        while queue:
            current = queue.popleft()

            for neighbor in self.graph.edges.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited

    def upstream(self, symbol_id: SymbolId) -> Set[SymbolId]:
        """
        Find all symbols that can affect `symbol_id`.
        (Traverse callee → caller)
        """
        visited: Set[SymbolId] = set()
        queue = deque([symbol_id])

        while queue:
            current = queue.popleft()

            for neighbor in self.graph.reverse_edges.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited
