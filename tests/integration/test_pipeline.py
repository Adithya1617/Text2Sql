from app.graph.pipeline import run_pipeline

def test_pipeline_runs_basic():
    res = run_pipeline("Top 5 merchants by transaction amount in July")
    assert res.table is not None
    assert "columns" in res.table
    assert "rows" in res.table
