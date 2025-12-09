import os
import shutil
import re
from typing import Generator, Dict, List, Tuple

import structlog
from rich.progress import Progress

from schrodinger.utils import ensure_directory


logger = structlog.stdlib.get_logger(__name__)


# Parse user extension inputs: "en: REGEX1; REGEX2" or "en"
def parse_extension_argument(ext_arg: str) -> Tuple[str, List[re.Pattern]]:
    """
    Convert user input like:
        "en"
        "en: EN_"
        "en: \\.en$ ; EN_"
    Into:
        ("en", [compiled_regex1, compiled_regex2])
    """

    if ":" not in ext_arg:
        # Use default fallback REGEX: endswith ".lang"
        lang = ext_arg.lower()
        return lang, [re.compile(rf"\.{lang}$", re.IGNORECASE)]

    lang, raw_regexes = ext_arg.split(":", 1)
    lang = lang.strip().lower()

    patterns = []
    for raw in raw_regexes.split(";"):
        r = raw.strip()
        if not r:
            continue
        patterns.append(re.compile(r, re.IGNORECASE))

    if not patterns:
        patterns.append(re.compile(rf"\.{lang}$", re.IGNORECASE))

    return lang, patterns


class Schrodinger:
    """
    REGEX-powered cloning engine.
    Creates a *new* output folder and copies:
        - language-matched files to ONLY their language
        - unclassified files to ALL languages
    """

    def __init__(self, base_path: str, extensions: List[str]):
        self.base_path = os.path.abspath(base_path)

        # Convert each extension input into: lang → [regex1, regex2, ...]
        self.lang_patterns: Dict[str, List[re.Pattern]] = {}

        for ext in extensions:
            lang, compiled = parse_extension_argument(ext)
            self.lang_patterns[lang] = compiled

        self.languages = list(self.lang_patterns.keys())

        self.output_root = os.path.join(
            os.path.dirname(self.base_path),
            "output"
        )
        ensure_directory(self.output_root)

        logger.info(
            "Initialized Schrodinger",
            base_path=self.base_path,
            output=self.output_root,
            langs=self.languages
        )

    # Determine which languages (if any) match file
    def classify_file(self, filename: str) -> List[str]:
        """
        Returns list of languages whose REGEX patterns match this file.
        Can return:
            []        → file belongs to ALL languages (unclassified)
            ["en"]    → en only
            ["en","hu"] → ambiguous overlap (we treat this as ERROR)
        """

        matches = []

        for lang, regex_list in self.lang_patterns.items():
            if any(pattern.search(filename) for pattern in regex_list):
                matches.append(lang)

        return matches


    # Generator: walk project and yield process items
    def matching_files(self) -> Generator[Tuple[str, str, str], None, None]:
        """
        Yields:
            abs_src, filename, rel_dir
        """

        for root, dirs, files in os.walk(self.base_path):
            # Prevent recursion into output folder
            dirs.clear()

            # Add only the directories we want to keep
            for d in os.listdir(root):
                if os.path.isdir(os.path.join(root, d)) and d.lower() not in self.languages and d != "output":
                    dirs.append(d)

            rel_dir = os.path.relpath(root, self.base_path)
            if rel_dir == ".":
                rel_dir = ""

            for filename in files:
                abs_src = os.path.join(root, filename)
                yield abs_src, filename, rel_dir


    def run(self) -> None:
        logger.info("Scanning files...")

        file_list = list(self.matching_files())

        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Copying files...", total=len(file_list)
            )

            for abs_src, filename, rel_dir in file_list:
                matched_langs = self.classify_file(filename)

                if len(matched_langs) > 1:
                    # Ambiguous file → user error
                    logger.error(
                        "Ambiguous REGEX match for file",
                        file=filename,
                        matched=matched_langs
                    )
                    continue

                if len(matched_langs) == 1:
                    # File belongs ONLY to one language
                    lang = matched_langs[0]
                    self.copy_to_language(abs_src, filename, rel_dir, lang)

                else:
                    # No regex matched → copy to ALL languages
                    for lang in self.languages:
                        self.copy_to_language(abs_src, filename, rel_dir, lang)

                progress.update(task, advance=1)

        logger.info("Finished!")
        print("\nDone! Your directories are ready.\n")


    def copy_to_language(self, abs_src: str, filename: str, rel_dir: str, lang: str):
        dest_dir = os.path.join(self.output_root, lang, rel_dir)
        ensure_directory(dest_dir)

        dest = os.path.join(dest_dir, filename)

        logger.debug(
            "Copying file",
            src=abs_src,
            dest=dest,
            lang=lang
        )

        shutil.copy2(abs_src, dest)
