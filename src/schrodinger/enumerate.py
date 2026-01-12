from pathlib import Path
from typing import List

def enumerate_paths(root_path: Path) -> List[Path]:
    if not root_path.exists():
        raise ValueError(f"Path does not exist: {root_path}")
    if not root_path.is_dir():
        raise ValueError(f"Path is not a directory: {root_path}")


    return [p.relative_to(root_path) for p in root_path.rglob("*") if p.is_file()]
