# src/pyimpact/analyzer/parser.py

import ast
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FunctionDefInfo:
    name: str
    lineno: int
    col_offset: int


@dataclass
class CallSiteInfo:
    caller: str
    callee: str
    lineno: int
    col_offset: int


class FunctionCallVisitor(ast.NodeVisitor):
    """
    AST visitor that collects function definitions and call sites.
    """

    def __init__(self) -> None:
        self.functions: list[FunctionDefInfo] = []
        self.calls: list[CallSiteInfo] = []
        self._current_function: Optional[str] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
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

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_Call(self, node: ast.Call):
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


def parse_python_file(path: Path) -> tuple[List[FunctionDefInfo], List[CallSiteInfo]]:
    """
    Parse a Python file and extract function definitions and call sites.
    """
    if not path.exists():
        raise FileNotFoundError(path)

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    visitor = FunctionCallVisitor()
    visitor.visit(tree)

    return visitor.functions, visitor.calls
