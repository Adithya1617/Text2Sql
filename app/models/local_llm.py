from datetime import datetime, timedelta
import re

def naive_intent_to_sql(question: str) -> str:
    q = question.lower()
    now = datetime.utcnow()
    last_30 = (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    july_year = now.year
    july_start = f"{july_year}-07-01 00:00:00"
    july_end = f"{july_year}-07-31 23:59:59"

    if "top" in q and "merchant" in q and "july" in q:
        m = re.search(r"top\s+(\d+)", q)
        top_n = int(m.group(1)) if m else 10
        return f"""
        SELECT m.name AS merchant, SUM(t.amount_cents)/100.0 AS total_amount
        FROM transactions t
        JOIN merchants m ON m.merchant_id = t.merchant_id
        WHERE t.txn_ts BETWEEN '{july_start}' AND '{july_end}'
        GROUP BY m.name
        ORDER BY total_amount DESC
        LIMIT {top_n}
        """

    m2 = re.search(r"merchant\s+([a-z0-9]+)", q)
    if ("total" in q or "sum" in q) and m2 and ("last 30" in q or "30 days" in q):
        merchant = m2.group(1).capitalize()
        return f"""
        SELECT m.name AS merchant, COUNT(*) AS txn_count, SUM(t.amount_cents)/100.0 AS total_amount
        FROM transactions t
        JOIN merchants m ON m.merchant_id = t.merchant_id
        WHERE m.name = '{merchant}' AND t.txn_ts >= '{last_30}'
        GROUP BY m.name
        ORDER BY total_amount DESC
        """

    return """
    SELECT m.name AS merchant, COUNT(*) AS txn_count, ROUND(AVG(t.amount_cents)/100.0, 2) AS avg_amount
    FROM transactions t
    JOIN merchants m ON m.merchant_id = t.merchant_id
    GROUP BY m.name
    ORDER BY txn_count DESC
    LIMIT 25
    """
