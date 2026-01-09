import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple

import structlog
from rich.progress import Progress

from schrodinger.utils import ensure_directory
from schrodinger.enumerate import enumerate_paths
from schrodinger.match import match_regexes
from schrodinger.copy import copy_directories

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
    def __init__(self, base_path: Path, extensions: List[str]):
        self.base_path = Path(os.path.abspath(base_path))

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
        self.output_root = Path(os.path.abspath(
            os.path.join(project_root, "..", "output")
        ))
        ensure_directory(self.output_root)

        logger.info(
            "Initialized Schrodinger",
            base_path=self.base_path,
            output=self.output_root,
            languages=self.languages,
        )
    # Execution
    def run(self) -> None:
        logger.info("Scanning files...")

        paths = enumerate_paths(self.base_path)
        matched = match_regexes(paths, self.language_patterns, full_path=False)
        copy_directories(matched, self.base_path, Path(self.output_root), self.languages)

        print("\n✔ Done! Your directories are ready.\n")
