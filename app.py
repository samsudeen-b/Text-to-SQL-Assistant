import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

# Load our secret API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- This describes our database structure to the AI ----
DB_SCHEMA = """
Table: customers
- customer_id (INTEGER, primary key)
- name (TEXT)
- city (TEXT)
- signup_date (TEXT)

Table: products
- product_id (INTEGER, primary key)
- product_name (TEXT)
- category (TEXT)
- price (REAL)

Table: orders
- order_id (INTEGER, primary key)
- customer_id (INTEGER, references customers)
- product_id (INTEGER, references products)
- quantity (INTEGER)
- order_date (TEXT)
"""

def generate_sql(question):
    """Send the user's question + schema to Groq, get back SQL only."""
    prompt = f"""You are an expert SQL assistant. Given this database schema:

{DB_SCHEMA}

Convert the following question into a single valid SQLite SQL query.
Only return the SQL query. No explanation, no markdown, no backticks.

Question: {question}
SQL Query:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    sql = response.choices[0].message.content.strip()

    # Clean up in case the model adds ```sql ... ``` anyway
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def run_query(sql):
    """Run the SQL against our SQLite database and return results as a DataFrame."""
    conn = sqlite3.connect("store.db")
    try:
        df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


# ------------------ STREAMLIT UI ------------------

st.set_page_config(page_title="Text-to-SQL Assistant", page_icon="🧠")
st.title("🧠 Intelligent Text-to-SQL Assistant")
st.write("Ask a question about the store database in plain English!")

# Example questions to help the user
with st.expander("💡 Example questions you can try"):
    st.write("""
    - Show all customers from Chennai
    - What is the total revenue from each product?
    - Who are the top 3 customers by number of orders?
    - List all products in the Electronics category
    - What is the average order quantity?
    """)

question = st.text_input("Type your question here:")

if st.button("Run Query"):
    if question.strip() == "":
        st.warning("Please type a question first!")
    else:
        with st.spinner("Thinking... generating SQL..."):
            sql_query = generate_sql(question)

        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

        with st.spinner("Running query..."):
            df, error = run_query(sql_query)

        if error:
            st.error(f"❌ Error running query: {error}")
        else:
            st.subheader("Results")
            if df is not None and len(df) > 0:
                st.dataframe(df)
                st.success(f"✅ Found {len(df)} result(s)")
            else:
                st.info("Query ran successfully but returned no results.")