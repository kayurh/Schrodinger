from pathlib import Path
from typing import Dict, List
import re

def match_regexes(
    paths: List[Path],
    language_patterns: Dict[str, List[re.Pattern]],
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
                    break

        if len(matched_languages) > 1:
            raise ValueError(
                f"Path '{relative_path}' matches multiple languages: "
                f"{matched_languages}"
            )

        matched_results[relative_path] = matched_languages

    return matched_results