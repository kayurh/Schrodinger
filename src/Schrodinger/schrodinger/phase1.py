from pathlib import Path
from typing import List


def enumerate_paths(root_path: Path) -> List[Path]:

    if not root_path.exists():
        raise ValueError(f"Path does not exist: {root_path}")

    if not root_path.is_dir():
        raise ValueError(f"Path is not a directory: {root_path}")

    enumerated_paths: List[Path] = []

    for item_path in root_path.iterdir():
        relative_item_path = item_path.relative_to(root_path)
        enumerated_paths.append(relative_item_path)

    return enumerated_paths


"""
HOW TO TEST: 
from pathlib import Path
from schrodinger.enumerate import enumerate_paths

paths = enumerate_paths(Path("examples/sample_project"))

for p in paths:
    print(p, type(p))
"""


"""
GIVEN:
sample_project/
├── file1.txt
├── file2.en
├── subdir/
│   └── file3.txt

OUTPUT: 
file1.txt
file2.en
subdir/ (Not subdir/file3.txt, Correct?)
"""
