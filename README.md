# Local Orchestrator: Offline-first NL → SQL (SQLite)

A **runnable starter scaffold** for the Local Orchestrator architecture.  

## Quick Start

```bash
# 1. Create environment
uv venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Initialize SQLite with sample data
uv run python setup/init_db.py

# 4. Start API (FastAPI, port 8000)
uv run uvicorn app.api.main:app --reload --port 8000

# 5. Start UI (Streamlit, port 8501)
uv run streamlit run app/ui/streamlit_app.py
```

## Tests
```bash
uv run pytest -q
```

## Project Layout
```
repo/
  README.md
  Makefile
  requirements.txt
  setup/init_db.py
  app/
    api/main.py
    graph/{nodes.py,pipeline.py}
    models/local_llm.py
    guards/sql_guard.py
    executors/sqlite_exec.py
    ui/streamlit_app.py
    utils/logger.py
  tests/
    unit/test_guard.py
    integration/test_pipeline.py
  app/data.db   # generated after running init_db.py
```
