# tests/unit/test_parser.py

from pathlib import Path

from pyimpact.analyzer.parser import parse_python_file


def test_parser_finds_functions():
    path = Path("tests/fixtures/parser_sample.py")

    functions, calls = parse_python_file(path)
    function_names = {f.name for f in functions}

    assert function_names == {"a", "b", "d"}


def test_parser_finds_call_sites():
    path = Path("tests/fixtures/parser_sample.py")

    _, calls = parse_python_file(path)
    call_pairs = {(c.caller, c.callee) for c in calls}

    assert ("a", "b") in call_pairs
    assert ("a", "c") in call_pairs
    assert ("d", "a") in call_pairs


def test_parser_ignores_top_level_calls(tmp_path):
    file = tmp_path / "top_level.py"
    file.write_text(
        """
print("hello")

def f():
    g()
"""
    )

    _, calls = parse_python_file(file)
    call_pairs = {(c.caller, c.callee) for c in calls}

    assert ("f", "g") in call_pairs
    assert len(call_pairs) == 1
