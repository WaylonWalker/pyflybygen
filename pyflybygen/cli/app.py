from pathlib import Path

import more_itertools
import typer

from pyflybygen.cli.common import verbose_callback
from pyflybygen.cli.config import config_app
from pyflybygen.cli.tui import tui_app
from pyflybygen.pyflybygen import get_imports

app = typer.Typer(
    name="pyflybygen",
    help="A rich terminal report for coveragepy.",
)
app.add_typer(config_app)
app.add_typer(tui_app)


def version_callback(value: bool) -> None:
    """Callback function to print the version of the pyflybygen package.

    Args:
        value (bool): Boolean value to determine if the version should be printed.

    Raises:
        typer.Exit: If the value is True, the version will be printed and the program will exit.

    Example:
        version_callback(True)
    """
    if value:
        from pyflybygen.__about__ import __version__

        typer.echo(f"{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    imports = more_itertools.flatten(
        [get_imports(p.read_text()) for p in Path(".").glob("**/*.py")]
    )
    print("\n".join(set(imports)))


if __name__ == "__main__":
    typer.run(main)
