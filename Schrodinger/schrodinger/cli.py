# For rich implementation
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time

# For argparse implementation:
import argparse
from rich.console import Console
from schrodinger.core import clone_directory_structure
from schrodinger.logger import log

console = Console()

def directory_summary(files):

    table = Table(title= "Directory Summary")
    table.add_column("Extension", justify="center")
    table.add_column("File Count", justify="right")

    for ext, count in files.items():
        table.add_row(ext, str(count))
    console.print(table)

def clone_files(files):
    console.print("Starting file duplication...")

    for file in track(files, description="Copying files..."):
        time.sleep(0.1)
    console.print("Duplication complete!")

# Testing to be implemented later
# Example output for rich
files = {".en": 23, ".hu": 19, ".txt": 42}
directory_summary(files)
clone_files(range(10))


def main():
    parser = argparse.ArgumentParser(
        description="Schrödinger — Clone files into a mirrored folder structure based on extensions."
    )

if __name__ == "__main__":
    main()

