from dataclasses import dataclass


@dataclass(frozen=True)
class SymbolId:
    """
    A stable, language-agnostic identifier for a code symbol
    (function, method, class, etc.).
    """

    language: str
    module: str
    qualname: str

    def __str__(self) -> str:
        return f"{self.language}:{self.module}:{self.qualname}"
