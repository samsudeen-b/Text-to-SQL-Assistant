\# QueryAI — AI-Powered Text-to-SQL Assistant



QueryAI is an AI-powered Text-to-SQL application that allows users to interact with a SQLite database using natural language.



Instead of writing SQL manually, users can ask questions such as:



> Show all customers from Chennai



QueryAI uses Groq's LLaMA model to convert the question into a SQL query, executes it against the database, and displays the results through a modern web interface.



\## Features



\- Natural language to SQL generation

\- Groq LLaMA integration

\- SQLite database

\- FastAPI backend

\- Modern responsive frontend

\- Generated SQL preview

\- Query result table

\- Read-only SQL protection

\- REST API

\- Swagger API documentation



┌─────────────────┐
│   User Question │
└────────┬────────┘
         ↓
┌─────────────────┐
│    Frontend     │
└────────┬────────┘
         ↓
┌─────────────────┐
│  FastAPI API    │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Groq LLaMA AI  │
│  Text → SQL     │
└────────┬────────┘
         ↓
┌─────────────────┐
│ SQLite Database │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Query Results   │
└─────────────────┘
