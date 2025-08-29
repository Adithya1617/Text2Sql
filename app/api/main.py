from fastapi import FastAPI
from pydantic import BaseModel
from ..graph.pipeline import run_pipeline

app = FastAPI(title="Local Orchestrator API", version="0.2.0")

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    res = run_pipeline(req.question)
    return {"explanation": res.explanation, "guard_reason": res.guard_reason, "table": res.table}

@app.get("/health")
def health():
    return {"status": "ok"}
