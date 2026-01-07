import os
import shutil
import re
from typing import Dict, List, Tuple, Generator

import structlog
from rich.progress import Progress

from schrodinger.utils import ensure_directory

logger = structlog.stdlib.get_logger(__name__)


# Parse user extension inputs
def parse_extension_argument(ext_arg: str) -> Tuple[str, List[re.Pattern]]:
    if ":" not in ext_arg:
        language = ext_arg.lower()
        return language, [re.compile(rf"\.{language}$", re.IGNORECASE)]

    language, raw_regexes = ext_arg.split(":", 1)
    language = language.strip().lower()

    compiled_patterns: List[re.Pattern] = []

    for raw_pattern in raw_regexes.split(";"):
        pattern_text = raw_pattern.strip()
        if pattern_text:
            compiled_patterns.append(re.compile(pattern_text, re.IGNORECASE))

    if not compiled_patterns:
        compiled_patterns.append(re.compile(rf"\.{language}$", re.IGNORECASE))

    return language, compiled_patterns


class Schrodinger:
    def __init__(self, base_path: str, extensions: List[str]):
        self.base_path = os.path.abspath(base_path)

        if not os.path.isdir(self.base_path):
            raise ValueError(f"Base path does not exist: {self.base_path}")

        # Parse language patterns
        self.language_patterns: Dict[str, List[re.Pattern]] = {}
        for ext in extensions:
            language, patterns = parse_extension_argument(ext)
            self.language_patterns[language] = patterns

        self.languages = list(self.language_patterns.keys())


        # Output directory
        project_root = os.path.dirname(self.base_path)  # examples/
        self.output_root = os.path.abspath(
            os.path.join(project_root, "..", "output")
        )
        ensure_directory(self.output_root)

        self.ambiguous_dir = os.path.join(self.output_root, "ambiguous")
        ensure_directory(self.ambiguous_dir)

        logger.info(
            "Initialized Schrodinger",
            base_path=self.base_path,
            output=self.output_root,
            languages=self.languages,
        )


    # Language classification
    def classify_file(self, filename: str) -> List[str]:
        matched_languages: List[str] = []

        for language, patterns in self.language_patterns.items():
            for pattern in patterns:
                if pattern.search(filename):
                    matched_languages.append(language)
                    break  # one match per language is enough

        return matched_languages


    # File enumeration
    def matching_files(self) -> Generator[Tuple[str, str, str], None, None]:
        output_abs = os.path.abspath(self.output_root)

        for root, dirs, files in os.walk(self.base_path):
            # Prevent recursion into output
            dirs[:] = [
                d for d in dirs
                if os.path.abspath(os.path.join(root, d)) != output_abs
            ]

            relative_dir = os.path.relpath(root, self.base_path)
            if relative_dir == ".":
                relative_dir = ""

            for filename in files:
                absolute_source = os.path.join(root, filename)
                yield absolute_source, filename, relative_dir


    # Execution
    def run(self) -> None:
        logger.info("Scanning files...")

        files = list(self.matching_files())

        with Progress() as progress:
            task = progress.add_task("Copying files...", total=len(files))

            for absolute_source, filename, relative_dir in files:
                matched_languages = self.classify_file(filename)

                # Ambiguous
                if len(matched_languages) > 1:
                    destination_dir = os.path.join(self.ambiguous_dir, relative_dir)
                    ensure_directory(destination_dir)
                    shutil.copy2(
                        absolute_source,
                        os.path.join(destination_dir, filename),
                    )
                    progress.update(task, advance=1)
                    continue

                # Single language
                if len(matched_languages) == 1:
                    self.copy_to_language(
                        absolute_source,
                        filename,
                        relative_dir,
                        matched_languages[0],
                    )
                else:
                    # Shared files (No extensions)
                    for language in self.languages:
                        self.copy_to_language(
                            absolute_source,
                            filename,
                            relative_dir,
                            language,
                        )

                progress.update(task, advance=1)

        print("\n✔ Done! Your directories are ready.\n")


    # Copy helper
    def copy_to_language(
        self,
        absolute_source: str,
        filename: str,
        relative_dir: str,
        language: str,
    ) -> None:
        destination_dir = os.path.join(self.output_root, language, relative_dir)
        ensure_directory(destination_dir)

        shutil.copy2(
            absolute_source,
            os.path.join(destination_dir, filename),
        )