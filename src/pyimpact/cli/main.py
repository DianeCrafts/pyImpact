import typer

app = typer.Typer(
    help="pyimpact: dependency graph + impact analysis for Python codebases"
)

@app.callback()
def main():
    """
    pyimpact: analyze Python codebases to understand function dependencies,
    impact of changes, dead code, and test scope.
    """
    pass


@app.command()
def hello():
    """Sanity check command."""
    typer.echo("pyimpact is installed and working ✅")
