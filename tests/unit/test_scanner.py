# tests/unit/test_scanner.py

from pathlib import Path

import pytest

from pyimpact.analyzer.scanner import scan_python_files


def test_scan_python_files_finds_expected_files():
    project_root = Path("tests/fixtures/sample_project")

    files = scan_python_files(project_root)
    filenames = {f.name for f in files}

    assert "a.py" in filenames
    assert "b.py" in filenames
    assert "c.py" in filenames


def test_scan_python_files_ignores_common_dirs():
    project_root = Path("tests/fixtures/sample_project")

    files = scan_python_files(project_root)
    paths = [str(f) for f in files]

    # Ensure ignored directories are not scanned
    assert not any("__pycache__" in p for p in paths)
    assert not any(".venv" in p for p in paths)


def test_scan_python_files_invalid_path():
    with pytest.raises(FileNotFoundError):
        scan_python_files(Path("does_not_exist"))


def test_scan_python_files_not_a_directory(tmp_path):
    file_path = tmp_path / "file.py"
    file_path.write_text("# not a directory")

    with pytest.raises(NotADirectoryError):
        scan_python_files(file_path)
