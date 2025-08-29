import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Local NL → SQL (Offline)", layout="wide")

st.title("🧠 Local NL → SQL (Offline)")
st.write("Talk to your local SQLite data. This demo uses a rule-based NL→SQL prototype with a safety guard.")

# Use environment variable or default, avoid st.secrets if not needed
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

question = st.text_input("Ask a question", value="Top 10 merchants by transaction amount in July")
if st.button("Ask"):
    with st.spinner("Running pipeline..."):
        r = requests.post(f"{API_URL}/ask", json={"question": question})
        if r.status_code == 200:
            data = r.json()
            st.caption(f"Guard: {data.get('guard_reason','')}")
            st.caption(data.get('explanation',''))
            table = data.get("table", {})
            rows = table.get("rows", [])
            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No rows returned.")
        else:
            st.error(f"API error: {r.status_code} - {r.text}")
