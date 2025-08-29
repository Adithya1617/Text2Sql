import pytest
from app.guards.sql_guard import enforce_read_only_and_limit

def test_blocks_ddl():
    with pytest.raises(ValueError):
        enforce_read_only_and_limit("DROP TABLE x;")

def test_injects_limit():
    sql, reason = enforce_read_only_and_limit("SELECT * FROM merchants")
    assert "LIMIT" in sql.upper()
    assert "cap" in reason.lower()

def test_ok_when_has_limit():
    s, reason = enforce_read_only_and_limit("SELECT * FROM merchants LIMIT 3")
    assert s.strip().upper().endswith("LIMIT 3")
    assert reason == "OK"
