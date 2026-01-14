from pathlib import Path
from typing import Dict, List
import shutil
import re

def copy_directories(
    matched_paths: Dict[Path, List[str]],
    language_patterns: Dict[str, List[re.Pattern]],
    input_root: Path,
    output_dir: Path,
    all_languages: List[str],
) -> None:

    for rel_path, languages in matched_paths.items():
        target_languages = languages if languages else all_languages

        src = input_root / rel_path
        if not src.is_file():
            continue

        for language_code in target_languages:
            cleaned_name = rel_path.name

            for regex in language_patterns.get(language_code, []):
                m = regex.search(cleaned_name)
                if m:
                    if "del" in m.groupdict() and m.group("del") is not None:
                        start, end = m.span("del")
                        cleaned_name = cleaned_name[:start] + cleaned_name[end:]
                    else:
                        raise ValueError("There was no 'del' group specified in regex.")
                    break

            cleaned_rel_path = rel_path.with_name(cleaned_name)

            dst = output_dir / language_code / cleaned_rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
