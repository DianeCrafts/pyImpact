from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Set

from .ids import SymbolId


@dataclass(frozen=True)
class CodeLocation:
    """
    Represents a precise location in a source file.
    """
    file_path: Path
    line: int
    column: int


@dataclass(frozen=True)
class FunctionSymbol:
    """
    Represents a function or method definition.
    """
    id: SymbolId
    name: str
    module: str
    location: CodeLocation
    is_async: bool = False
    class_name: Optional[str] = None


@dataclass(frozen=True)
class CallSite:
    """
    Represents a call from one symbol to another.
    """
    caller_id: SymbolId
    callee_name: str
    callee_id: Optional[SymbolId]
    location: CodeLocation


@dataclass
class DependencyGraph:
    """
    Directed graph representing symbol dependencies.
    """
    nodes: Dict[SymbolId, FunctionSymbol] = field(default_factory=dict)
    edges: Dict[SymbolId, Set[SymbolId]] = field(default_factory=dict)
    reverse_edges: Dict[SymbolId, Set[SymbolId]] = field(default_factory=dict)

    def add_node(self, symbol: FunctionSymbol) -> None:
        """Add a symbol to the graph."""
        self.nodes[symbol.id] = symbol
        self.edges.setdefault(symbol.id, set())
        self.reverse_edges.setdefault(symbol.id, set())

    def add_edge(self, caller: SymbolId, callee: SymbolId) -> None:
        """Add a directed edge caller → callee."""
        self.edges.setdefault(caller, set()).add(callee)
        self.reverse_edges.setdefault(callee, set()).add(caller)
