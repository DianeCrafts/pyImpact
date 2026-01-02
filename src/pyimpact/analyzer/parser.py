import ast
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


# =========================
# Data transfer objects
# =========================

@dataclass
class FunctionDefInfo:
    """
    Lightweight representation of a function definition.
    """
    name: str
    lineno: int
    col_offset: int


@dataclass
class CallSiteInfo:
    """
    Lightweight representation of a function call inside another function.
    """
    caller: str
    callee: str
    lineno: int
    col_offset: int


@dataclass
class ImportInfo:
    """
    Represents an import statement.

    Examples:
      from a.b import c as d
        module="a.b", name="c", alias="d"

      import a.b as c
        module="a.b", name=None, alias="c"
    """
    module: str
    name: Optional[str]
    alias: Optional[str]


# =========================
# AST Visitor
# =========================

class FunctionCallVisitor(ast.NodeVisitor):
    """
    AST visitor that collects:
    - function definitions
    - call sites inside functions
    - import statements
    """

    def __init__(self) -> None:
        self.functions: List[FunctionDefInfo] = []
        self.calls: List[CallSiteInfo] = []
        self.imports: List[ImportInfo] = []

        self._current_function: Optional[str] = None

    # -------- Function definitions --------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions.append(
            FunctionDefInfo(
                name=node.name,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )

        previous = self._current_function
        self._current_function = node.name

        self.generic_visit(node)

        self._current_function = previous

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    # -------- Function calls --------

    def visit_Call(self, node: ast.Call) -> None:
        if self._current_function is not None:
            callee_name = self._extract_callee_name(node.func)
            if callee_name:
                self.calls.append(
                    CallSiteInfo(
                        caller=self._current_function,
                        callee=callee_name,
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                    )
                )

        self.generic_visit(node)

    def _extract_callee_name(self, node: ast.AST) -> Optional[str]:
        """
        Extract function name from a call node.

        Examples:
          foo()        -> foo
          mod.foo()    -> foo
          self.foo()   -> foo
        """
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None

    # -------- Imports --------

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=node.module or "",
                    name=alias.name,
                    alias=alias.asname,
                )
            )

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(
                ImportInfo(
                    module=alias.name,
                    name=None,
                    alias=alias.asname,
                )
            )


# =========================
# Public API
# =========================

def parse_python_file(
    path: Path,
) -> tuple[
    List[FunctionDefInfo],
    List[CallSiteInfo],
    List[ImportInfo],
]:
    """
    Parse a Python file and extract:
    - function definitions
    - call sites
    - import statements

    This function is Python-specific but returns language-agnostic
    data structures suitable for graph construction and resolution.
    """
    if not path.exists():
        raise FileNotFoundError(path)

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    visitor = FunctionCallVisitor()
    visitor.visit(tree)

    return visitor.functions, visitor.calls, visitor.imports
