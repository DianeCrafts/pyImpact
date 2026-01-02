from pathlib import Path
import typer
from pyimpact.app.callers import run_callers
from pyimpact.app.callees import run_callees
from pyimpact.app.impact import run_impact_analysis
from pyimpact.app.visualize import visualize
from pyimpact.query.subgraph import SubgraphMode


app = typer.Typer(
    help="pyimpact: dependency graph + impact analysis for Python codebases"
)


@app.callback()
def main():
    """Analyze Python codebases to understand dependencies and impact."""
    pass


@app.command()
def hello():
    """Sanity check command."""
    typer.echo("pyimpact is installed and working ✅")


@app.command()
def impact(function: str, path: Path = Path(".")):
    """Visualize impact graph for a function."""
    visualize(function, path, SubgraphMode.IMPACT)



@app.command()
def callers(function: str, path: Path = Path(".")):
    """Visualize callers graph for a function."""
    visualize(function, path, SubgraphMode.CALLERS)




@app.command()
def callees(function: str, path: Path = Path(".")):
    """Visualize callees graph for a function."""
    visualize(function, path, SubgraphMode.CALLEES)



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
