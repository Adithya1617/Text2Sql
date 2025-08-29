.PHONY: install db api ui test demo

install:
	uv venv && . .venv/bin/activate && uv pip install -r requirements.txt

db:
	uv run python setup/init_db.py

api:
	uv run uvicorn app.api.main:app --reload --port 8000

ui:
	uv run streamlit run app/ui/streamlit_app.py

test:
	uv run pytest -q

demo: install db api
