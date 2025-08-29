from dataclasses import dataclass
from typing import Any, Dict
from ..models.sql_agent import question_to_sql
from ..guards.sql_guard import enforce_read_only_and_limit
from ..executors.sqlite_exec import run_sql

@dataclass
class Intent:
    raw: str
    parsed: Dict[str, Any]

@dataclass
class Plan:
    steps: list
    sql: str = ""

@dataclass
class GuardedSQL:
    sql: str
    reason: str

@dataclass
class ExecutionResult:
    rows: list
    columns: list
    elapsed_sec: float
    error: str = None

@dataclass
class Result:
    table: Any
    explanation: str
    guard_reason: str



def parse_intent(question: str) -> Intent:
    return Intent(raw=question, parsed={})

def plan_query(intent: Intent) -> Plan:
    return Plan(steps=["parse", "generate_sql", "guard", "execute"])

def generate_sql(plan: Plan, question: str) -> Plan:
    sql = question_to_sql(question)
    plan.sql = sql
    return plan

def guard_sql(plan: Plan) -> GuardedSQL:
    safe_sql, reason = enforce_read_only_and_limit(plan.sql)
    return GuardedSQL(sql=safe_sql, reason=reason)

def execute_sql(guarded: GuardedSQL) -> ExecutionResult:
    return run_sql(guarded.sql)
