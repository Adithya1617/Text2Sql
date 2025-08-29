import sqlite3, contextlib, pathlib, time

DB_PATH = pathlib.Path(__file__).resolve().parents[1] / "data.db"

def run_sql(sql: str, timeout_s: float = 3.0):
    start = time.time()
    with contextlib.closing(sqlite3.connect(DB_PATH, timeout=timeout_s)) as conn:
        conn.row_factory = sqlite3.Row
        with contextlib.closing(conn.cursor()) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    elapsed = time.time() - start
    cols = rows[0].keys() if rows else []
    data = [dict(r) for r in rows]
    return {"columns": list(cols), "rows": data, "elapsed_sec": round(elapsed, 4)}
