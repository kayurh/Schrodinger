from pathlib import Path
from typing import Dict, List
import re


def _match_regexes(
    paths: List[Path],
    language_patterns: Dict[str, List[re.Pattern]],
    *, # Improves clarity. Argument must be "full_path=True" not "True"
    full_path: bool = False,) -> Dict[Path, List[str]]:

    matched_results: Dict[Path, List[str]] = {}

    for relative_path in paths:
        matched_languages: List[str] = []

        # Decide what string to test against regexes
        if full_path:
            match_target = str(relative_path)
        else:
            match_target = relative_path.name

        for language_code, regex_list in language_patterns.items():
            for regex in regex_list:
                if regex.search(match_target):
                    matched_languages.append(language_code)
                    break  # Language found

        # A file must not match multiple languages
        if len(matched_languages) > 1:
            raise ValueError(
                f"Path '{relative_path}' matches multiple languages: "
                f"{matched_languages}"
            )

        matched_results[relative_path] = matched_languages

    return matched_results


"""
HOW TO TEST: 
from pathlib import Path
import re

paths = [
    Path("EN_readme.txt"),
    Path("HU_readme.txt"),
    Path("notes.txt"),
]

language_patterns = {
    "en": [re.compile(r"^EN_")],
    "hu": [re.compile(r"^HU_")],
}

results = match_regexes(paths, language_patterns, full_path=False)
"""


"""
OUTPUT:
{
   Path("EN_readme.txt"): ["en"],
   Path("HU_readme.txt"): ["hu"],
   Path("notes.txt"): []
}
"""

