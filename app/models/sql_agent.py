from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.llms import Ollama
import pathlib
import re

DB_PATH = pathlib.Path(__file__).resolve().parents[1] / "data.db"

def get_sql_agent():
    # Connect to SQLite
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # Load local LLM
    llm = Ollama(model="mistral")

    # Create SQL query chain - this returns SQL only, doesn't execute
    return create_sql_query_chain(llm, db)

def clean_sql_output(sql_text: str) -> str:
    """Clean SQL output by removing markdown, comments, and extra formatting."""
    # Remove markdown code blocks
    sql_text = re.sub(r'```sql\n?', '', sql_text)
    sql_text = re.sub(r'```\n?', '', sql_text)
    
    # Remove leading/trailing whitespace
    sql_text = sql_text.strip()
    
    # Split by lines and filter out comments/explanations
    lines = sql_text.split('\n')
    sql_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines and comment lines
        if line and not line.startswith('--') and not line.startswith('#'):
            sql_lines.append(line)
    
    # Join back together
    clean_sql = ' '.join(sql_lines)
    
    # Basic validation - ensure it starts with SELECT
    if not clean_sql.upper().startswith('SELECT'):
        # Try to extract SELECT statement if it exists
        select_match = re.search(r'(SELECT\s+.*?)(?:;|\n|$)', clean_sql, re.IGNORECASE | re.DOTALL)
        if select_match:
            clean_sql = select_match.group(1).strip()
        else:
            return "SELECT 'Invalid SQL generated' as error;"
    
    # Ensure SQL ends properly (remove trailing semicolon if present, we'll add it back)
    clean_sql = clean_sql.rstrip(';').strip()
    
    # Add semicolon back
    clean_sql += ';'
    
    return clean_sql

def question_to_sql(question: str) -> str:
    """Generate SQL for a natural language question."""
    try:
        agent = get_sql_agent()
        raw_response = agent.invoke({"question": question})
        
        # Clean the SQL output
        sql = clean_sql_output(str(raw_response))
        
        print(f"Raw response: {raw_response}")  # Debug logging
        print(f"Cleaned SQL: {sql}")  # Debug logging
        
        return sql
        
    except Exception as e:
        print(f"Error generating SQL: {e}")
        # Return a safe fallback query
        return "SELECT 'Error generating SQL' as error;"
