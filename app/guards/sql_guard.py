import re
from typing import Tuple

READ_ONLY_PATTERN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE|ATTACH|DETACH)\b", re.I)

def enforce_read_only_and_limit(sql: str, default_limit: int = 100) -> Tuple[str, str]:
    s = sql.strip().rstrip(";")
    if READ_ONLY_PATTERN.search(s):
        raise ValueError("Blocked: non read-only SQL detected.")
    if s.lower().startswith("select") and " limit " not in s.lower():
        s = f"{s} LIMIT {default_limit}"
        return s, f"LIMIT injected to cap result size at {default_limit}."
    return s, "OK"
