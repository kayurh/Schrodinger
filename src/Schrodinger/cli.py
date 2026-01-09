# cli.py
import argparse
from rich.console import Console
from rich.table import Table

from schrodinger import Schrodinger

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Schrodinger — Clone and organize directories by language/regex."
    )

    parser.add_argument("path", help="Base folder containing files to copy")
    parser.add_argument(
        "-v", "--extensions", nargs="+", required=True,
        help='Language-regex pairs, e.g. "en: ^EN_ ; \\.en$" "hu: ^HU_ ; \\.hu$"'
    )

    args = parser.parse_args()

    console.rule("[bold cyan]Schrodinger Tool")
    table = Table(title="Execution Summary")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Base Path", args.path)
    table.add_row("Extensions", ", ".join(args.extensions))
    console.print(table)

    sch = Schrodinger(args.path, args.extensions)
    sch.run()

if __name__ == "__main__":
    main()