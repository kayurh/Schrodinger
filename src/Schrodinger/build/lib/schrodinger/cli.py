import argparse
import re
from rich.console import Console
from rich.table import Table
from schrodinger.core import Schrodinger, parse_extension_argument

console = Console()


def parse_cli_extensions(ext_list):
    """
    Convert CLI inputs like:
        ["en", "hu: HU_"]
    Into a list suitable for Schrodinger constructor:
        ["en: \.en$", "hu: HU_"]
    """
    parsed = []
    for ext in ext_list:
        lang, patterns = parse_extension_argument(ext)
        # Recombine into string format for Schrodinger
        regex_strs = " ; ".join(p.pattern for p in patterns)
        parsed.append(f"{lang}: {regex_strs}")
    return parsed


def main():
    parser = argparse.ArgumentParser(
        description="Schrodinger — Clone and organize directories by language/regex."
    )

    parser.add_argument(
        "path",
        help="Base folder containing files to copy"
    )

    parser.add_argument(
        "-v", "--extensions",
        nargs="+",
        required=True,
        help='Language-regex pairs, e.g., "en: \.en$ ; EN_" "hu: HU_"'
    )

    parser.add_argument(
        "--full-path",
        action="store_true",
        help="Recursively traverse the entire directory tree (currently handled in core)"
    )

    args = parser.parse_args()

    # Parse extensions for Schrodinger
    parsed_extensions = parse_cli_extensions(args.extensions)

    # Show execution summary
    console.rule("[bold cyan]Schrodinger Tool")
    table = Table(title="Execution Summary")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Base Path", args.path)
    table.add_row("Extensions", ", ".join(parsed_extensions))
    table.add_row("Full Path", str(args.full_path))

    console.print(table)

    # Initialize Schrodinger with regex-driven extensions
    sch = Schrodinger(args.path, parsed_extensions)

    # Run the copying/cloning process
    sch.run()

    console.print("\n[bold green]✔ Done![/] Your directories are ready.\n")


if __name__ == "__main__":
    main()
