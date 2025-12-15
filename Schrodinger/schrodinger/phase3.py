from pathlib import Path
from typing import Dict, List
import shutil


def _copy_directories(
    matched_paths: Dict[Path, List[str]],
    output_dir: Path,) -> None:

    # Collect all language extensions
    all_languages: set[str] = set()

    for languages in matched_paths.values():
        all_languages.update(languages)

    for source_path, languages in matched_paths.items():
        # No extension therefore copy to all languages
        target_languages = languages or list(all_languages)

        for language_code in target_languages:
            destination_path = output_dir / language_code / source_path

            # Ensure parent directories exist
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source_path, destination_path)
