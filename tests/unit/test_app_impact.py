from pyimpact.app.impact import run_impact_analysis


def test_run_impact_analysis_simple_project(tmp_path):
    """
    a() -> b()
    b() -> pass
    """
    file = tmp_path / "a.py"
    file.write_text(
        """
def a():
    b()

def b():
    pass
"""
    )

    graph, target, downstream, upstream = run_impact_analysis("a", tmp_path)

    assert target.qualname == "a"

    downstream_names = {s.qualname for s in downstream}
    upstream_names = {s.qualname for s in upstream}

    assert downstream_names == {"b"}
    assert upstream_names == set()
