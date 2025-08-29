from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Intent:
    raw: str
    parsed: Dict[str, Any]

@dataclass
class Plan:
    steps: list
    sql: Optional[str] = None

@dataclass
class Result:
    table: Dict[str, Any]
    explanation: str
    guard_reason: str = "OK"
