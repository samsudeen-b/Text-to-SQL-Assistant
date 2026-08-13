import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

load_dotenv()

app = FastAPI(title="QueryAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DB_PATH = "store.db"

DB_SCHEMA = """
Table: customers
- customer_id INTEGER PRIMARY KEY
- name TEXT
- city TEXT
- signup_date TEXT

Table: products
- product_id INTEGER PRIMARY KEY
- product_name TEXT
- category TEXT
- price REAL

Table: orders
- order_id INTEGER PRIMARY KEY
- customer_id INTEGER
- product_id INTEGER
- quantity INTEGER
- order_date TEXT
"""


class QueryRequest(BaseModel):
    question: str


def generate_sql(question):
    prompt = f"""
You are an expert SQLite SQL assistant.

Database schema:
{DB_SCHEMA}

Convert the user's question into ONE read-only SQLite SELECT query.

Rules:
- Return ONLY SQL.
- Only SELECT statements are allowed.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or PRAGMA.

Question:
{question}

SQL:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    return (
        response.choices[0].message.content
        .strip()
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )


def run_query(sql):
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(sql, conn)
        return df
    finally:
        conn.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/query")
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        sql = generate_sql(request.question)
        df = run_query(sql)

        return {
            "question": request.question,
            "sql": sql,
            "columns": list(df.columns),
            "rows": df.fillna("").to_dict(orient="records"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))