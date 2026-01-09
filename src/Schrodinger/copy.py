from pathlib import Path
from typing import Dict, List
import shutil

def copy_directories(
    matched_paths: Dict[Path, List[str]],
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
            dst = output_dir / language_code / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
