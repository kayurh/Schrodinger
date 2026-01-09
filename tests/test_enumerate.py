from pathlib import Path

from schrodinger.phase1 import *


def test_enumerate_returns_direct_children_only():
    """Ensure only immediate children of sample_dir are listed."""

    root = Path(__file__).parent / "sample_dir"

    items = enumerate_paths(root)

    # Convert Paths to simple string names
    names = sorted([p.as_posix() for p in items])

    # What exists directly inside sample_dir?
    expected = sorted([
        "sample_sub_1",
        "sample_sub_2",
        "test_text.md.en",
        "test_text.md.en.hu",
        "test_text.md.hu",
        "test_text.png",
    ])

    assert names == expected


def test_paths_are_relative():
    """Returned items must be relative Path objects, not absolute."""

    root = Path(__file__).parent / "sample_dir"
    items = enumerate_paths(root)

    assert len(items) > 0

    for p in items:
        assert not p.is_absolute()
        # Should be single-component paths like "file.txt" or "folder"
        assert len(p.parts) == 1


def test_nonexistent_path_raises():
    """If the root directory doesn't exist, a ValueError must be raised."""

    nonexistent = Path("this/path/does/not/exist")

    try:
        enumerate_paths(nonexistent)
    except ValueError as e:
        assert "does not exist" in str(e)
    else:
        raise AssertionError("Expected ValueError for missing path")


def test_non_directory_path_raises(tmp_path):
    """If the path exists but is not a directory, raise ValueError."""

    file_path = tmp_path / "not_a_directory.txt"
    file_path.write_text("hello", encoding="utf-8")

    try:
        enumerate_paths(file_path)
    except ValueError as e:
        assert "not a directory" in str(e)
    else:
        raise AssertionError("Expected ValueError for non-directory")
