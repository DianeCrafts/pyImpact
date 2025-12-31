from pathlib import Path

from pyimpact.app.impact import run_impact_analysis
from pyimpact.core.ids import SymbolId


def run_callees(
    function_name: str,
    project_root: Path,
) -> set[SymbolId]:
    """
    Find all functions called by the given function.
    """
    downstream, _ = run_impact_analysis(function_name, project_root)
    return downstream
