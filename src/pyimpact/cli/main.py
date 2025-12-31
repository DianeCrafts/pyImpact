from pathlib import Path
import typer

from pyimpact.app.impact import run_impact_analysis

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
def impact(
    function: str,
    path: Path = typer.Argument(
        Path("."),
        exists=True,
        file_okay=False,
        dir_okay=True,
        help="Project root directory (defaults to current directory)",
    ),
):

    """
    Show impact analysis for a function in a project.
    """
    downstream, upstream = run_impact_analysis(function, path)

    typer.echo(f"\nImpact analysis for function: {function}\n")

    typer.echo("Affected (downstream):")
    if downstream:
        for s in downstream:
            typer.echo(f"  - {s.qualname}")
    else:
        typer.echo("  (none)")

    typer.echo("\nAffected by (upstream):")
    if upstream:
        for s in upstream:
            typer.echo(f"  - {s.qualname}")
    else:
        typer.echo("  (none)")
