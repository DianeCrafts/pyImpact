# src/pyimpact/analyzer/scanner.py

from pathlib import Path

# Directories we never want to scan
IGNORED_DIRS = {
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".git",
    "dist",
    "build",
    ".eggs",
}


def scan_python_files(root: Path) -> list[Path]:
    """
    Recursively scan a directory and return all Python (.py) files,
    excluding common ignored directories.

    Args:
        root: Path to the project root

    Returns:
        List of absolute Paths to Python files
    """
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    python_files: list[Path] = []

    for path in root.rglob("*.py"):
        # Skip files inside ignored directories
        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        python_files.append(path.resolve())

    return python_files
