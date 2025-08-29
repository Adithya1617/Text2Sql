from .nodes import Intent, Plan, Result
from ..models.local_llm import naive_intent_to_sql
from ..guards.sql_guard import enforce_read_only_and_limit
from ..executors.sqlite_exec import run_sql

def run_pipeline(question: str) -> Result:
    intent = Intent(raw=question, parsed={})
    plan = Plan(steps=["parse","retrieve_schema","plan","generate_sql","guard","execute","postprocess"])
    sql = naive_intent_to_sql(question)
    plan.sql = sql
    safe_sql, reason = enforce_read_only_and_limit(sql)
    table = run_sql(safe_sql)
    explanation = "Answer from rule-based NL→SQL prototype. Swap with LangGraph + LLM for production."
    return Result(table=table, explanation=explanation, guard_reason=reason)
