from pathlib import Path
from pyimpact.app.impact import run_impact_analysis
from pyimpact.core.ids import SymbolId


def run_callees(
    function_name: str,
    project_root: Path,
) -> tuple[SymbolId, set[SymbolId]]:
    _, target, downstream, _ = run_impact_analysis(function_name, project_root)
    return target, downstream
