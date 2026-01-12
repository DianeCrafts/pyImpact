from pathlib import Path
import typer

from pyimpact.app.impact import run_impact_analysis
from pyimpact.app.colors import impact_colors
from pyimpact.app.visualize import visualize_svg
from pyimpact.query.subgraph import extract_subgraph
from pyimpact.reporting.graphviz import render_svg

app = typer.Typer(
    help="pyimpact: dependency graph + impact analysis for Python codebases"
)


@app.command()
def impact(function: str, path: Path = Path(".")):
    """
    Visualize full impact (callers + callees).
    """
    graph, target, downstream, upstream = run_impact_analysis(function, path)

    nodes, edges = extract_subgraph(
        graph=graph,
        target=target,
        upstream=upstream,
        downstream=downstream,
    )

    roles = impact_colors(target, upstream, downstream)
    dot = render_svg(nodes, edges, roles)
    visualize_svg(dot)


@app.command()
def callers(function: str, path: Path = Path(".")):
    """
    Visualize callers only.
    """
    graph, target, _, upstream = run_impact_analysis(function, path)

    nodes, edges = extract_subgraph(
        graph=graph,
        target=target,
        upstream=upstream,
        downstream=set(),
    )

    roles = impact_colors(target, upstream, set())
    dot = render_svg(nodes, edges, roles)
    visualize_svg(dot)


@app.command()
def callees(function: str, path: Path = Path(".")):
    """
    Visualize callees only.
    """
    graph, target, downstream, _ = run_impact_analysis(function, path)

    nodes, edges = extract_subgraph(
        graph=graph,
        target=target,
        upstream=set(),
        downstream=downstream,
    )

    roles = impact_colors(target, set(), downstream)
    dot = render_svg(nodes, edges, roles)
    visualize_svg(dot)


# @app.command()
# def impact(
#     function: str,
#     path: Path = typer.Argument(
#         Path("."),
#         exists=True,
#         file_okay=False,
#         dir_okay=True,
#         help="Project root directory (defaults to current directoclsry)",
#     ),
# ):
#     """
#     Show impact analysis for a function in a project.
#     """
#     downstream, upstream = run_impact_analysis(function, path)

#     typer.echo(f"\nImpact analysis for function: {function}\n")

#     typer.echo("Affected (downstream):")
#     if downstream:
#         for s in downstream:
#             typer.echo(f"  - {s.qualname}")
#     else:
#         typer.echo("  (none)")

#     typer.echo("\nAffected by (upstream):")
#     if upstream:
#         for s in upstream:
#             typer.echo(f"  - {s.qualname}")
#     else:
#         typer.echo("  (none)")


# @app.command()
# def callers(
#     function: str,
#     path: Path = typer.Argument(
#         Path("."),
#         exists=True,
#         file_okay=False,
#         dir_okay=True,
#         help="Project root directory (defaults to current directory)",
#     ),
# ):
#     """
#     Show all functions that call the given function.
#     """
#     callers_set = run_callers(function, path)

#     typer.echo(f"\nCallers of function: {function}\n")

#     if callers_set:
#         for s in callers_set:
#             typer.echo(f"  - {s.qualname}")
#     else:
#         typer.echo("  (none)")


# @app.command()
# def callees(
#     function: str,
#     path: Path = typer.Argument(
#         Path("."),
#         exists=True,
#         file_okay=False,
#         dir_okay=True,
#         help="Project root directory (defaults to current directory)",
#     ),
# ):
#     """
#     Show all functions called by the given function.
#     """
#     callees_set = run_callees(function, path)

#     typer.echo(f"\nCallees of function: {function}\n")

#     if callees_set:
#         for s in callees_set:
#             typer.echo(f"  - {s.qualname}")
#     else:
#         typer.echo("  (none)")
