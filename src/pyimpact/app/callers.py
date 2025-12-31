from pathlib import Path

from pyimpact.app.impact import run_impact_analysis
from pyimpact.core.ids import SymbolId


def run_callers(
    function_name: str,
    project_root: Path,
) -> set[SymbolId]:
    """
    Find all functions that call the given function.
    """
    _, upstream = run_impact_analysis(function_name, project_root)
    return upstream
