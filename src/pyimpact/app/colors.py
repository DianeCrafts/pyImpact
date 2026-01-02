from pyimpact.core.ids import SymbolId


def impact_colors(
    target: SymbolId,
    upstream: set[SymbolId],
    downstream: set[SymbolId],
) -> dict[SymbolId, str]:
    """
    Decide node colors for impact visualization.
    """
    colors: dict[SymbolId, str] = {}

    colors[target] = "target"

    for s in upstream:
        colors[s] = "upstream"

    for s in downstream:
        colors[s] = "downstream"

    return colors
